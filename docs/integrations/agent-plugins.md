<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abducer for Codex and Claude Code

The `abducer` plugin exposes 221 public research skills from `skills/*/*/SKILL.md`
and all 34 normalized workflow contracts in both hosts. It includes the read-only
`abducer-workflows` MCP server. Native research routing uses a writable Abducer
checkout; contract inspection works from the installed package alone. Installing
the plugin does not install the research runtime.

The flat plugin entry skills resolve and read the canonical skill in that
checkout. Scripts, references, KBs, state and validators retain their existing
paths. Research runs in the checkout. The plugin bundles no native hooks,
credentials, or research datasets. Its MCP server only reads the packaged
workflow catalog and never launches a scientific workflow.

## Prepare a research workspace

Clone this repository and provision its existing runtime:

```bash
git clone https://gitlab.idiap.ch/neurosymbolicai/abducer.git
cd abducer
uv sync --locked
```

Start the host in this checkout or one of its subdirectories. To use a checkout
while working elsewhere, set its absolute path before launching your host:

```bash
export ABDUCER_ROOT="/absolute/path/to/abducer"
```

An explicitly set root takes precedence over directory discovery. Each entry
resolves the requested source and checks its SHA-256 against the plugin inventory.
If source versions differ, regenerate and reinstall from that checkout. An
absent checkout, unknown skill or missing source stops the route with setup
instructions. Individual workflows may additionally need provider credentials,
Lean or LaTeX; follow their canonical instructions.

## Install in Codex

From the repository root:

```bash
codex plugin marketplace add .
codex plugin add abducer@abducer
```

The catalog is `.agents/plugins/marketplace.json`, and its plugin path is
`./plugins/abducer`. In a desktop client that exposes repo marketplaces, open
the plugin directory, select **Abducer**, and install **abducer**. Start a new
session after installation. For example, invoke `$abducer:kb-orchestrator` and
give it a KB target and bounded task, or `$abducer:work` for one work-loop step.

## Install in Claude Code

Inside Claude Code, replace the path below with your absolute checkout path:

```text
/plugin marketplace add /absolute/path/to/abducer
/plugin install abducer@abducer
```

The catalog is `.claude-plugin/marketplace.json`. Restart the session, then use
`/abducer:kb-orchestrator` or `/abducer:work` with your intended target and budget.
For temporary development loading, start from the checkout with:

```bash
claude --plugin-dir ./plugins/abducer
```

For distribution from the existing GitLab remote, both hosts can register the
Git repository URL instead of a local path once these changes are committed and
pushed. That requires access to the repository. This work does not publish it.

## Which skills are exposed?

`plugins/abducer/source-skills.json` is the complete inventory, including source
paths, descriptions and digests. Public orchestration, reasoning, ingestion,
discovery, evaluation, proof-delivery, reporting, control-plane, manuscript and
Yang–Mills skills are included. The public `cohere-fast-orchestrator` retains
its explicit activation procedure.

The deeper `skills/domain_specific/ym` implementations are private to cohere-fast
and are reached through its receipt gates. Many reuse public Yang–Mills names.
Generic Yang–Mills requests do not activate cohere-fast. Complete `proj_skills`,
`prism_me` and preserved `external` skill packs are not exported. The normalized
workflow entries do expose their specifically mapped development/support owners;
private domain prerequisites still apply to native execution.

## Normalized workflows and MCP

`plugins/abducer/workflows.json` contains every canonical normalized workflow ID,
namespace, version, native aliases, owner, descriptor digest and complete contract.
There are 34 additional `workflow-...` skill entries, giving 255 total plugin
entries. Names use client-compatible hyphens while preserving underscore IDs in
the contracts. For example:

| Surface | Proof-delivery contract |
| --- | --- |
| Codex skill | `$abducer:workflow-theorem-proof-delivery` |
| Claude Code skill | `/abducer:workflow-theorem-proof-delivery` |
| MCP tool | `get_workflow` with `{"workflow_id":"theorem_proof_delivery_workflow"}` |
| MCP prompt | `theorem_proof_delivery_workflow` |
| MCP resource | `abducer://workflows/theorem_proof_delivery_workflow` |

`list_workflows` returns the full inventory, including the mapping to each plugin
entry. All 34 also appear in MCP `prompts/list` and `resources/list`. Both tools
are read-only. The server serves an immutable catalog snapshot; restart it after
updating the package. It accepts canonical IDs, not arbitrary filesystem paths.

Every contract retains draft/interface-only status and its declared binding,
payload and internal-control gaps. Inspecting a workflow never supplies a missing
executor, satisfies opt-in activation, validates a proof or approves publication.
Native execution can be requested separately through its original skill and
gates. The checkout resolver supports `--workflow <canonical-id>` and verifies
both descriptor and owning-skill digests before returning their source paths.

Host installation automatically discovers the packaged MCP launch configuration:
portable `mcp.json`, Codex compatibility `.codex-mcp.json`, and Claude Code's
`.mcp.json`. Each starts the same bundled standard-library Python server with
its host's plugin-root placeholder. No shell command, model service, network
listener, SDK installation or credential is needed for catalog inspection.

For another MCP client, configure a stdio server with `command: python3` and the
single argument `/absolute/path/to/abducer/plugins/abducer/scripts/workflow_mcp.py`.
To run that entry point directly:

```bash
python3 /absolute/path/to/abducer/plugins/abducer/scripts/workflow_mcp.py
```

The server follows the [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
using newline-delimited JSON-RPC on stdin/stdout;
it is not an interactive shell. Source-tree development can instead launch
`integrations/workflow_mcp/server.py` after regenerating the package.

Refresh the marketplace, reinstall plugin version 0.2.0 and restart the host to
load the new workflow entries and MCP server in an existing installation. These
repository changes do not modify your user-level plugin cache automatically.

Plugin installation and successful command execution establish neither a proof
nor scientific progress. The original evidence, claim ceilings and validators
continue to govern every research output.

## Maintain the package

Edit the canonical skill, not its generated plugin entry. From the root:

```bash
uv run python agentic/scripts/normalize_workflow_skills.py --check
uv run python integrations/agent_plugins/generate.py
uv run python integrations/agent_plugins/generate.py --check
uv run pytest -q tests/integrations/test_agent_plugins.py tests/integrations/test_workflow_mcp.py tests/orchestration/test_workflow_skill_v1_projection.py
```

Commit the regenerated entries and inventory alongside source changes. Adjust
`integrations/agent_plugins/metadata.json` for release metadata and bump its
version for a published update. Refresh the marketplace and reinstall the plugin
to update a host's cached copy. The resolver and this guide are maintained
directly; the generator owns the manifests, catalogs, inventory and entry skills.
Edit `integrations/workflow_mcp/server.py` for MCP behavior; the generator copies
it to the plugin. Do not edit the bundled server or workflow catalog separately.

Both hosts use `plugins/abducer`. Root `hooks/hooks.json` remains an internal
Abducer registry and is never installed as native host hooks. Local agent settings
remain ignored; only the Codex marketplace catalog is exposed under `.agents`.

Canonical `skills/**/SKILL.md` and generated plugin skill files carry their
licensing through `REUSE.toml`, without inline license comments. Canonical notices
retain their original copyright, contributor and group attribution. The plugin
includes its own generated `REUSE.toml` so its annotations also travel with an
installed or distributed copy.

The package follows the supported [OpenAI plugin layout](https://developers.openai.com/plugins/build/plugins)
and [Claude Code plugin manifest layout](https://code.claude.com/docs/en/plugins-reference).
Codex's compatibility manifest is included alongside the portable manifest.

## Read source assets through MCP

The source-checkout MCP server can export the exact public skill instructions,
workflow descriptors, and declared schema/provenance files for clients such as
Lunar. This is a source snapshot, not a research execution service. Existing
workflow resources, prompts and list/get tools keep their read-only behavior.

Call `list_agent_assets` with `{}` and follow each returned `next_cursor` using
`{"cursor":"100"}` (use the actual cursor returned, not a hardcoded offset).
Each page identifies source-relative paths, kinds and SHA-256 digests. Then call
`read_agent_asset` with an exact returned key, for example
`{"path":"skills/orchestration/work/SKILL.md"}` only if that key was listed.
Decode the returned `encoding` (`text` or `base64`) and verify the bytes against
`sha256`. Reads return this session's frozen snapshot; scripts are bytes to
inspect and grant no authority to execute, prove, publish or promote anything.

Run the server from this checkout, for example
`python3 integrations/workflow_mcp/server.py`. The generated server under
`plugins/abducer/scripts/` supports the same asset reads while it remains in this
checkout. An independently installed routing-only plugin still exposes workflow
contracts but reports that complete asset export requires the source checkout:
it cannot invent the original schemas/provenance or search an unrelated project.
Keep its original workflow inspection available, and configure a source-checkout
connection when a client needs full conversion. If native source digests changed,
refresh the native generated catalogs before retrying with a new server session.

The public manifests select ordinary and workflow entry skills. Private workflow
owners may be included as reference bytes without becoming independently public
skills. Paths outside the declared closure, credential files and symlink escapes
are rejected; there is no arbitrary filesystem read or native execution RPC.
