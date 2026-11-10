<!-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch> -->
<!-- SPDX-License-Identifier: MIT -->
# Abducer in ChatGPT

**Live private deployment:** https://abducer.andrenfreitas.chatgpt.site — version 8,
published on 2026-10-25 through Sites. ChatGPT confirms the provisioned **Abducer**
plugin is installed. Open a new chat and select `@Abducer` if its tools are not yet
visible. This deployment supports canonical skill/workflow exploration, personal
projects and a signed connection to the native Python worker on the owner's Mac.
Live authenticated `get_profile` confirms worker readiness and native hooks.
Discovery Marathon is admitted; conceptual artifact validation is available;
other complete workflow routes remain gated. See [Native execution from ChatGPT](chatgpt-native-execution.md).

For a user walkthrough, open the [interactive field guide](https://abducer.andrenfreitas.chatgpt.site/tutorial): two detailed investigations in mathematical and physical abduction. Reconstruct Dini’s theorem through a compactness bridge and audit its assumptions; derive three damping laws, compare held-out predictions and design a discriminating experiment. Interactive controls, canonical skill mappings and copyable prompts connect the reasoning to saved research projects. The Explorer header links to it as **Field guide**. Its [standalone HTML source](../../integrations/chatgpt/sites/tutorial.html) also opens locally without a build or external assets.

For the connected local executor, see [Native execution from ChatGPT](chatgpt-native-execution.md).
It preserves the original runner and hook scripts, and can obtain model responses
from the current ChatGPT conversation. The container-service sections below
describe the alternative standalone service with its own OAuth and model API.

The generated client v0.2.0 also carries a verified native hook source bundle.
See [Exporting workflow hooks](chatgpt-hook-fidelity.md) for its five-event
contract, reproducible ZIP command, host mappings and current execution gaps.
Exporting these sources does not install or activate global ChatGPT hooks.

The hosted profile connects Explorer and five entry skills to an authenticated Abducer service. It reuses the canonical 221-skill library, 34 workflow contracts, 19 typed viewer graphs, and the existing native Discovery Marathon adapter. The original checkout-backed plugin remains available at `plugins/abducer`.

The hosted source profile at `plugins/abducer-chatgpt` deliberately has no endpoint. Generate a configured release only after supplying an actual HTTPS service URL. Installing the package does not deploy the service, provision users, or supply model credentials.

## What is implemented

Named users can create private projects, inspect canonical skills and workflow graphs, prepare a bounded research plan, queue a native cycle, poll or cancel it, and read digest-verified reports. Explorer uses the MCP Apps bridge and is available as an ordinary rendered tool, sidebar entry, or conversation panel where the host supports those extensions.

All skills and contracts are inspectable. Only the explicitly registered Discovery Marathon workflow is admitted for hosted execution, and only with a verified immutable runtime snapshot and operator-enabled worker. Its initial targets are P versus NP and Yang–Mills. Other scientific procedures remain behind their existing orchestration and prerequisites; the service does not expose arbitrary shell execution or claim every graph is executable.

Research runs use the native prepare/execute/verify adapter. Initialization can legitimately produce a revision-required result with zero research cycles. A verified report means the native execution/report identity checks passed; it does not establish scientific truth. Failure never substitutes an old report.

## Prepare the development environment

```sh
uv sync --locked --group chatgpt
uv run --group chatgpt python integrations/agent_plugins/generate.py
uv run --group chatgpt python -m integrations.chatgpt.generate_plugin --check
uv run --group chatgpt pytest -q tests/integrations/test_chatgpt_*.py
```

The hosted dependency group is opt-in. Existing scientific dependencies and local stdio behavior are preserved. The native generator recreates ignored local marketplace metadata when needed; hosted generation writes a separate package.

## Build a deployable source snapshot

Run from the repository root, using a new directory outside the checkout:

```sh
uv run --group chatgpt python -m integrations.chatgpt.deployment \
  --source-root . --output /tmp/abducer-container
cd /tmp/abducer-container
cp .env.example .env
```

The builder uses the existing domain export source-selection policy, adds the required public catalog files, verifies source stability, and records every selected file's digest. It excludes unselected research runs, local configuration, environments and credential files. Review the manifest and selected dataset/license content before distributing the worker image. Unlike the client package, the worker image contains the selected research runtime and KB sources.

Edit `.env` with the actual public HTTPS origin, exact OAuth issuer, JWKS URL and required scope. The example domain is a placeholder. `ABDUCER_PUBLIC_URL` is the origin/base path without a trailing slash; the token audience must be exactly that value plus `/mcp`. Do not put credentials in Git or plugin files.

```sh
docker compose build
docker compose up -d service
```

The service listens on host loopback port 8000 by default. Put a production HTTPS reverse proxy in front of it, preserving the canonical host and forwarding the `/mcp`, `/.well-known/oauth-protected-resource/mcp`, and health routes. Preserve authorization headers and allow MCP response bodies; avoid caching authenticated responses. Configure TLS, request/rate limits and logs in the selected hosting platform. The image runs as a non-root user, with a read-only source filesystem and writable research volume.

This initial deployment is single-host: service and worker share SQLite and the artifact volume. Do not scale replicas across unrelated disks or place SQLite on an unreliable shared filesystem. Moving to a distributed database/queue is a separate deployment change with its own concurrency tests.

## Connect named users

Use an OAuth/OIDC provider supporting authorization code with PKCE S256 and the MCP resource audience. Configure a predefined client or a supported client-registration mode, and use the exact callback supplied by ChatGPT. The service publishes protected-resource metadata and validates signed access tokens against the configured issuer, audience, expiry, scope and provisioned subject. The identity provider owns the login screen and authorization flow; Abducer does not issue passwords or tokens.

Provision each account with its **stable issuer subject**, obtained from the identity provider. A display name or email address is not an authorization key:

```sh
docker compose exec service python -m integrations.chatgpt.server provision-user \
  --subject 'ISSUER_SUBJECT' --name 'Researcher name'
```

New projects are private to their creator. An operator can grant a colleague access:

```sh
docker compose exec service python -m integrations.chatgpt.server grant-project \
  --subject 'COLLEAGUE_SUBJECT' --project-id 'PROJECT_ID' --role viewer
```

Roles are `viewer`, `researcher`, and `admin`; research changes require researcher/admin membership. Sharing grants are operator CLI operations, not model-selected permission changes. Disable a user with the same provisioning command and `--disabled`. Revoked users fail new requests, and the worker rechecks authority while a job runs and before publication.

Local account disabling is checked immediately. Issuer-side token revocation is subject to token expiry and the issuer's key-rotation behavior; this JWT verifier does not perform token introspection. Choose appropriately short access-token lifetimes at the identity provider.

Provider-specific setup must enable the scope advertised by the service and return the exact audience. Refer to the current [OpenAI authentication guidance](https://developers.openai.com/plugins/build/auth) when registering the real provider/client. A successful local signed-token test does not substitute for testing that provider's interactive login in ChatGPT.

## Enable research execution

Configure `ABDUCER_MODEL` and `OPENAI_API_KEY` in the worker environment. `OPENAI_BASE_URL` defaults to the Responses API endpoint and may be replaced with an operator-controlled compatible HTTPS endpoint. These are backend credentials and costs; a user's ChatGPT subscription is not a model API budget.

Set `ABDUCER_WORKER_ENABLED=true` in `.env`, then start the research profile:

```sh
docker compose --profile research up -d
```

Each plan has an expiry, exact project/state parent, source release, full runtime digest, and limits for wall-clock time, model calls and per-call output tokens. Current native initialization needs a 32,000-output-token ceiling; the service rejects lower incompatible ceilings before work begins. Model calls may still fail, be refused or require revision. Limits bound resource use, not scientific quality or a precise currency price.

The native public-literature adapter permits only its declared Crossref/arXiv API reads. A new run requires explicit public-network permission. No user-supplied command or arbitrary URL becomes a worker entrypoint.

The supervisor uses a separate process group per job and kills it on cancellation, timeout or lease loss. It preserves private diagnostics and publishes reports only after verification. A lost worker is recorded as failed rather than replayed automatically, because the provider may have completed a paid call. Retrying a start with the same idempotency key retrieves the original job.

Successful state is saved as a digest-bound workspace checkpoint. A subsequent job copies that checkpoint and re-enters the canonical gate. Stale or consumed scientific authorization is a legitimate failure requiring a newly admissible canonical state; the hosted adapter does not manufacture a receipt or bypass the gate to force continuation. Process/workspace separation does not offer a sandbox for executing arbitrary user code; that capability is intentionally absent.

## Package and connect the plugin

From the repository checkout, generate to a separate release directory with the real service endpoint:

```sh
uv run --group chatgpt python -m integrations.chatgpt.generate_plugin \
  --endpoint https://YOUR_HOST/mcp --output /tmp/abducer-plugin-release
uv run --group chatgpt python -m integrations.chatgpt.generate_plugin \
  --endpoint https://YOUR_HOST/mcp --output /tmp/abducer-plugin-release --check
```

Connect the custom MCP service in ChatGPT using its supported developer/plugin flow, complete OAuth with a provisioned account, then install the configured plugin package through the available testing/distribution route. The five skills are `abducer-setup`, `abducer-explore`, `abducer-plan`, `abducer-research`, and `abducer-report`. They coordinate canonical procedures through the tools and never require a local checkout.

An end-to-end acceptance conversation is: “Open my research project and explain the conceptual hypothesis workflow”; “Prepare one Discovery Marathon cycle for P versus NP within these limits”; “Start that plan”; “Show the resulting report and distinguish evidence from hypotheses.” Check the returned plan and job identity at each transition. The conceptual diagram itself is not the executable job identifier.

The generated package includes skill/contract/viewer inventories and source hashes. Keep the service and client package on a matched source release. Public directory submission, privacy/terms URLs, screenshots and provider domain verification are operator release steps; no submission or public deployment is implied by this repository change. See [plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Operate and upgrade

Use `/healthz` for process readiness, job status for research outcomes, and the private worker log for diagnostics. Health alone does not prove model credentials, public literature access or scientific readiness. Protect and retain the research volume according to your project's policy; it includes prompts, artifacts and state.

For backups, stop new admissions and drain/cancel active jobs, then take a consistent database and artifact-volume backup together. Preserve the exact immutable source image for each checkpoint. Deploy new code as a new image and regenerate catalogs/client inventories; old prepared plans must fail version checks. Existing checkpoints from a different runtime release are not silently migrated. Restore the matching image and data backup for rollback.

The hosted CI workflow tests the service, worker boundary, plugin generation and existing integrations, then builds and checks the immutable image. The local test suite uses controlled model/worker fixtures where stated. Live model research, interactive external OAuth, public deployment and directory acceptance require configured external services and separate recorded evidence.
# ChatGPT Sites deployment

The private Sites deployment is the account-hosted route used by Zh Research
Explorer. It supplies hosting, ChatGPT sign-in, D1 storage and a provisioned MCP
plugin without a separate Plugin Creator installation or external OAuth setup.
The Abducer adapter lives in `integrations/chatgpt/sites/`; its managed source
checkout is `sites/abducer/`, versioned separately by the Sites source helper.

This version exposes all 221 canonical skills, 34 workflow contracts and 19 graphs,
plus private per-user research projects, revision-checked notes, and research plans.
ChatGPT reads canonical skills and conducts supported research in the conversation.
Its signed native bridge can connect to a separately running Python worker.
Use `get_execution_capabilities` to check current worker readiness and admitted
workflow coverage. Discovery Marathon uses its native adapter and hook scripts;
conceptual maps can be checked by the original validator. These checks do not
certify scientific truth. COHERE and other workflows retain their execution gates.
Required external tools and source dependencies remain explicit.

To rebuild the private Sites adapter from the canonical catalog:

```bash
.venv/bin/python -m integrations.chatgpt.sites_export --output /tmp/abducer-library.json
node integrations/chatgpt/sites/build.mjs /tmp/abducer-library.json sites/abducer https://abducer.andrenfreitas.chatgpt.site
node tests/infrastructure/chatgpt_sites_worker.mjs /tmp/abducer-library.json
```

The managed checkout must also run `bash scripts/build.sh` and
`node scripts/validate-artifact.mjs` before packaging. The latter checks that
`dist/server/index.js` equals the generated `worker/index.js`; packaging stale
build output does not publish the current source behavior.

Publish the managed checkout through the Sites source helper and native deployment
tools, preserving its `.openai/hosting.json` project ID. Do not replace this ID with
the Zh project's ID or copy its sharing settings. The new Abducer site starts
owner-private. Sites publication creates its MCP plugin; use the returned plugin
connection ID to offer installation, or find it under Plugins → Personal → Created
by you. Sharing with additional named users is a separate explicit access change.

Projects are keyed by Sites' authenticated user ID. Writes require identity,
same-origin browser requests, and optimistic revision checks. Each user can keep
100 projects, with up to 100 notes and 48,000 total serialized note characters per
project. Skill and source excerpts are paginated. Catalog and project operations
need no backend model credential. Connected native jobs have separate bounded
admission and private storage; ChatGPT mode pauses at each requested model response,
while the optional API provider uses the operator's model credentials.

## Dependencies at setup and startup

The generated plugin now includes a locked runtime installer and launch command.
See [setup and loading](chatgpt-native-execution.md#setup-and-loading) for the one-command host startup.
All declared project and ChatGPT runtime packages install into a dedicated environment;
service and worker startup eagerly load canonical skills, workflow manifests, graphs
and supporting source files. Explorer and `get_profile` show the resulting readiness.
This does not start research or grant execution support to unqualified workflows.
