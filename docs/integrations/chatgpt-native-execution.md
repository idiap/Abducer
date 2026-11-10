<!-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch> -->
<!-- SPDX-License-Identifier: MIT -->
# Native execution from ChatGPT

This guide explains how the private Abducer plugin connects to the repository's
native executor. It is for users starting research runs and operators maintaining
the local bridge. Catalog visibility, executable workflow coverage and scientific
validity are distinct statuses.

For portable source packaging and exact hook/host mappings, see
[Exporting workflow hooks](chatgpt-hook-fidelity.md). The export includes a
verifiable native hook bundle while retaining explicit gaps in prompt and
exception/cancellation lifecycle coverage.

## Setup and loading

The plugin uses a prepared Abducer host. Open Explorer or call `get_profile` to
see `dependency_setup`: startup imports the twelve declared runtime libraries and
loads all 221 skills, 34 workflow dependency manifests and 19 graphs. Supporting
sources are cached before requests are served. Missing packages or sources remain
visible in readiness; only already-qualified workflows become executable.

The exported plugin includes `runtime-setup/pyproject.toml`, `uv.lock` and a
stdlib-only installer. On the host, use Python matching `pyproject.toml`
(currently 3.11 or newer) and uv:

```bash
python runtime-setup/setup_runtime.py \
  --environment /absolute/writable/abducer-env \
  --source-root /absolute/abducer-source \
  --launch bridge -- --host 127.0.0.1 --port 8766
```

The command installs every locked project and ChatGPT runtime dependency, checks
package consistency, then launches the bridge in that environment. Repeat it for
idempotent startup; use `--launch worker` for the worker, or `--launch server`
for the standalone MCP service. Add `--code-root` when integration code and the
immutable scientific snapshot are released separately. Configure the existing
private identity/provider settings in the operator environment before launch.
Omit `--launch` to install only. Docker installs the same dependency group at build
time and preloads sources at process startup. Existing shared Python environments
are never overwritten; the installer requires a dedicated destination outside the
source or installed plugin tree.

Loading does not start a research run, import arbitrary skill scripts, install
other account plugins, or inject every source document into ChatGPT's context.
The hosted plugin's onboarding reads readiness from the already-prepared service;
it cannot run a local shell inside your online ChatGPT account.

For this integration, the Python environment belongs to the Abducer execution
host, currently the owner's Mac. Explorer and its MCP tools run on Sites and
connect to that host through the signed bridge. ChatGPT's separate Data Analysis
or Code Interpreter environment is not the environment prepared by this setup.

Some canonical skill documents retain historical commands such as
`.venv-pmp/bin/python`. New deployment snapshots include compatibility launchers
at `.venv/bin/python`, `.venv/bin/python3`, `.venv-pmp/bin/python` and
`.venv-pmp/bin/python3`. These execute the same managed interpreter selected by
the bootstrap's `PYTHON` variable; they do not duplicate environments or modify
canonical skill instructions. Direct operator use must set `PYTHON` to the
absolute managed interpreter first. Launchers reject missing, relative or
recursive interpreter targets. The environment verification command exercises
all four paths. Workflow execution still requires its qualified adapter,
external capabilities and authored research inputs.

## Open a run's reasoning HTML

In Explorer, select **My research → your project → a completed run**. Select
`full_timeline.html` (or `latest.html`), then **Open reasoning HTML**. Abducer loads
every page and verifies the complete document against its published SHA-256
before opening the original report. Its timeline, tabs and embedded mathematics
remain interactive. **Download original HTML** saves the exact published file
for offline reading; the source excerpt remains available for inspection.

The same controls appear under **Reports** in the standalone MCP Explorer. In
ChatGPT, ask: “Open the reasoning HTML for run <run ID>.” The assistant should
resolve an artifact from that run and open Explorer, without starting research.

Reports are retrieved from your authenticated native executor, so it must be
online. Large self-contained timelines load in bounded pages, with progress;
the reader supports documents up to 64 MiB. Report scripts run in an isolated
frame with external requests disabled. Downloads retain the original bytes.
Changing project or report cancels display of an old selection. A hash mismatch
or incomplete download produces an error rather than a partial HTML report.

Only artifacts actually published by the selected run appear. The existing
deployment acceptance runs failed or were cancelled and published no reports;
they cannot display historical reports as if those runs produced them. Report
availability and successful rendering do not establish scientific correctness.

## Deployed local connection

The private Sites deployment is live at https://abducer.andrenfreitas.chatgpt.site.
The authenticated plugin profile confirmed the native worker, `chatgpt` model
provider and native hooks on 2026-10-25. Open a new ChatGPT conversation and select
Abducer if the current conversation still shows its previous tool list. Explorer's
**My research** panel also exposes native planning, start, status and cancellation.

The executor and private state live under `~/.local/share/abducer/native/`.
`setup-runtime.json` contains the local configuration and secret; keep it private.
`worker.pid`, `bridge.pid` and their logs identify the running local processes.
Both processes use a dedicated environment and separately versioned integration
code. Their PID files and the paths in the private operator configuration identify
the active releases; do not assume that an older environment directory is active.
Prior configurations and releases remain available for rollback. The scientific
source snapshot has its exact file inventory and digest in `.abducer-source.json`.
Configuration, installed environments and research state remain outside the repository.
This deployment uses a temporary HTTPS tunnel: the Mac and tunnel must remain
online, and a changed tunnel URL must be updated in Sites and redeployed.

Live acceptance exercised a native model request and consumed an actual
conversation-authored research charter, then enforced the one-call test budget.
A second run was cancelled while awaiting a response. The original conceptual
validator rejected an intentionally empty map and persisted its hook receipt.
Neither run advanced a checkpoint. These are operational checks, not a completed
scientific cycle or proof. Original local workflow regressions also pass.

## What runs where

Explorer and the plugin remain on Sites. An authenticated server-side bridge
submits bounded operations to the Python service. A local worker executes a
versioned copy of the native sources in a separate writable workspace. The
existing runner, validators and native hook scripts retain their authority.

Discovery Marathon has a full native adapter. Conceptual hypothesis exploration
has an original artifact validator that can check an authored map; that operation
does not generate candidates or complete the whole abductive workflow. COHERE
Fast has a native state-machine adapter requiring a real child executor and
explicit domain activation. Its disabled domain gates are preserved. The other
normalized contracts remain inspectable until their execution paths qualify.

`get_execution_capabilities` reports current source-bound worker readiness and
per-workflow coverage. A configured URL or an old completed run does not establish
that a compatible worker is online now.

## Run with reasoning in ChatGPT

1. Select Abducer in ChatGPT and create or choose a private research project.
2. Inspect `get_execution_capabilities` and the workflow's dependencies. Read the
   canonical owner skill and relevant source before preparing a run.
3. Use `prepare_research_run` with an admitted workflow, target and bounded budget.
   Inspect the returned plan, then call `start_research_run` with a unique
   idempotency key. Retain the key when recovering an uncertain start.
4. Poll `get_run_status`. When `model_handoff_waiting` is true, read every page of
   `get_pending_model_request`. It contains the runner's actual messages and JSON
   output schema. Produce the requested research response and submit its JSON
   text with `submit_model_response` and the exact request ID.
5. The worker validates and consumes the response, executes its next native step,
   and may request another response. On completion, inspect its recorded outcome,
   hook coverage and verified report artifacts. Use `cancel_run` to stop early.

This is an actual native run with a conversational model provider. It pauses when
ChatGPT has not supplied a requested answer; it is not unattended background
reasoning. Model-call count, execution time and response bytes are bounded. The
native requested output-token allowance is guidance in this mode because MCP
does not report ChatGPT's token usage. The separate API provider continues to pass
the allowance to the model API.

The model response must contain genuine reasoning or explicit uncertainty. Never
submit invented experiment results, validator receipts or proof certificates to
make a run progress. Schema acceptance is not scientific verification.

For a conceptual map, use `validate_hypothesis_map` with the owned project and
the actual map JSON. Read its verdict, diagnostics and hook receipt. Recover
previous operations through `list_validation_receipts` and
`get_validation_receipt`; a validator success alone does not run the whole workflow.

## Preserve hook semantics

The native adapter uses `hooks/hooks.json` and the original `hooks/scripts`.
`UserPromptSubmit` and `PreSkillUse` surround the native owner invocation;
`PreToolUse` checks the instrumented effects; `PostSkillUse` checks artifacts;
`Stop` applies the original stop policy. JSON `block` remains blocking even when
the hook process exits with status zero. Native warnings remain warnings.

Internal operators are not automatically separate host skill invocations. The
returned coverage names the events and effect boundaries actually observed. It
does not claim every filesystem write or unrelated ChatGPT action was intercepted.
The stricter optional `hooks/workflow_local` policies are not silently substituted.

## Operator configuration

Create a sanitized immutable source snapshot with the existing deployment tooling:

```sh
/absolute/writable/abducer-env/bin/python -m integrations.chatgpt.runtime snapshot \
  --source-root . --output /absolute/private/path/source
```

Use `--help` to confirm the installed CLI arguments. Keep research data and local
credentials outside the repository and outside the immutable source directory.
The local bridge uses these settings:

| Setting | Purpose |
| --- | --- |
| `ABDUCER_REPOSITORY_ROOT` | Verified source snapshot directory |
| `ABDUCER_DATA_ROOT` | Private SQLite database, jobs and artifacts |
| `ABDUCER_WORKER_ENABLED=true` | Operator enables native admission |
| `ABDUCER_NATIVE_HOOKS_ENABLED=true` | Execute original native lifecycle policies |
| `ABDUCER_MODEL_PROVIDER=chatgpt` | Obtain native model responses through ChatGPT |
| `ABDUCER_NATIVE_BRIDGE_AUDIENCE` | Exact Sites project ID |
| `ABDUCER_NATIVE_BRIDGE_KEY` | 32 random bytes encoded as 64 hex characters |
| `ABDUCER_NATIVE_BRIDGE_SUBJECTS_JSON` | Explicit mapping from Sites-scoped subject IDs to provisioned backend users |

Provision the backend user through `Store.provision_user` or the existing operator
CLI. The bridge does not create accounts from submitted email addresses. Configure
the same audience and signing key in Sites server secrets, plus
`ABDUCER_NATIVE_BRIDGE_URL` pointing at the HTTPS service. Never expose that key in
Explorer, a tool argument, source control or the hosting manifest.

From the exported package, start the two local processes using the configured
operator environment. Each command synchronizes dependencies before launching:

```sh
python runtime-setup/setup_runtime.py \
  --environment /absolute/writable/abducer-env \
  --source-root /absolute/abducer-source \
  --launch bridge -- --host 127.0.0.1 --port 8766

python runtime-setup/setup_runtime.py \
  --environment /absolute/writable/abducer-env \
  --source-root /absolute/abducer-source \
  --launch worker
```

Add `--code-root /absolute/integration-release` to both commands when using a
separate integration release. The source, data directory and provisioned identity
mapping must agree between the bridge and worker.

### Container configuration

The Docker image installs the same locked project and ChatGPT dependency groups.
The supplied Compose recipe retains its standalone OAuth/API defaults:
`ABDUCER_MODEL_PROVIDER=api` and `ABDUCER_NATIVE_HOOKS_ENABLED=false`. Both settings
are explicitly configurable in the worker environment. Select native hook
execution with `ABDUCER_NATIVE_HOOKS_ENABLED=true`; selecting the `chatgpt`
provider additionally requires a configured signed bridge sharing the worker's
SQLite database and artifact volume. That bridge exposes
`get_pending_model_request` and `submit_model_response`; the standalone OAuth
MCP server does not expose these handoff operations. Changing the provider variable
alone does not supply the bridge. The Compose recipe still requires its OAuth
configuration and service health check, so use the two-process bridge deployment
above for the existing ChatGPT connection.

Expose only the authenticated bridge through an HTTPS tunnel. A temporary tunnel
is suitable for establishing local parity, and its URL may change on restart.
For continuous availability use a stable tunnel or hosted executor. The Mac must
remain online while it is the execution host. Updating Sites environment values
requires a deployment to apply them.

## Interpret failures and continuation

An unavailable worker, missing source dependency, disabled domain, native policy
block, expired model request or failed validator remains a real failure. The
service does not substitute an older report. An uncertain start should be queried
or retried with its original idempotency key; a new key can create different work.

Only verified successful work advances a research checkpoint. Cancellation and
failure preserve diagnostic state without claiming scientific completion. Source
changes require a new verified snapshot and compatible worker; checkpoint source
or target mismatches are rejected rather than silently migrated.
