<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Getting started

Install the environment and complete a first example. This section is for readers learning or using Abducer.

Use Python 3.11 or newer and the committed `uv.lock` environment:

```bash
uv sync --locked
uv run python skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py --help
uv run python agentic/scripts/run_canonical_discovery_cycle.py --help
```

These commands inspect both execution surfaces without launching a research run.
The default local path does not require provider credentials. Read the
[first-use guide](README.md) before selecting a target: some
commands intentionally write canonical target state and are unsuitable as disposable
smoke tests.

## Read next

- [Execution surfaces](../getting-started/execution-surfaces.md) — Choose theorem assistance or canonical discovery.
- [Operations](../operations/README.md) — Run and observe maintained workflows.
- [Named workflows](../architecture/named-workflows.md) — Choose activation and stopping conditions.
- [Plugins](../integrations/agent-plugins.md) — Discover public research skills.

Return to the [documentation index](../README.md) or consult the
[documentation map](../reference/documentation-map.md) for the complete retained collections.

## Inspect a concrete target without running it

Open [the P-vs-NP KB](../../KB/p-vs-np.kb.md) and its
[case-study index](../case-studies/pvsnp/README.md). Identify the source claims,
open obligations, and evidence limits before selecting an executable route.
Use the [execution-surface guide](execution-surfaces.md) to choose the matching runtime.
Both `--help` checks above are inspection steps; a research run must use the target,
state, and artifact contracts in the corresponding runbook.
