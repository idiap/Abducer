<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abducer plugin

This package exposes 221 public research skills and all 34 normalized workflow
contracts in Codex and Claude Code, plus the read-only `abducer-workflows` MCP server.
Each entry reads its canonical instructions from a writable Abducer checkout.
Workflow contracts are also bundled for inspection without a checkout.

Clone `https://gitlab.idiap.ch/neurosymbolicai/abducer.git`, run `uv sync --locked`
there, and start your host in that checkout. Alternatively, set `ABDUCER_ROOT`
to its absolute path before launching your host. Python 3.11 or later is required
by the checkout resolver. The plugin does not include the research runtime.

Use `$abducer:kb-orchestrator` in Codex or `/abducer:kb-orchestrator` in Claude
Code with your target and bounded task. `work` coordinates a persistent work-loop
step. Source evidence and validation gates determine what the outputs establish.

Use `$abducer:workflow-theorem-proof-delivery` in Codex or
`/abducer:workflow-theorem-proof-delivery` in Claude Code to inspect a normalized
workflow. Every normalized ID has a `workflow-...` entry in both hosts;
`workflows.json` records the complete ID/entry/owner mapping. The bundled MCP
server exposes `list_workflows`, `get_workflow`, 34 prompts and 34 resources.
Its standard-library Python process requires no extra package installation.

Normalized workflows remain draft and interface-only. Contract inspection and
MCP retrieval add no execution adapter or scientific authority. Native execution
still follows its canonical skill, checkout, opt-in and domain receipt gates.

`source-skills.json` records source paths and digests. A version mismatch stops
the route: regenerate with `uv run python integrations/agent_plugins/generate.py`
in the checkout, refresh your marketplace, then reinstall the plugin. Never run
research from this installed directory. See `docs/integrations/agent-plugins.md`
in the checkout for complete installation and maintenance instructions.
