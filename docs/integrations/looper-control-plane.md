<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Looper Control Plane

Abducer now has a Looper-style control plane for target-oriented work. The
domain engine remains the existing `skills/` tree: KB grounding, connector
analysis, hypothesis generation, proof queues, work cycles, and reports.

Looper adds governance around that engine:

- target packets under `agentic/examples/targets/` and
  `agentic/state/current_target.json`;
- recursive dependency graphs under `agentic/state/dependency_graphs/`;
- visible workflow manifests under `registry/tasks/`;
- transparent hooks under `hooks/`;
- workflow contracts and gate policy under `agentic/registries/`;
- compliance, drift, frame-adequacy, reachability, and release reports under
  `agentic/reports/`;
- structured TODO cards under `agentic/todos/`.

## Visible Unit

The visible unit is the workflow, not the individual skill. For example,
`registry/tasks/p-vs-np-target-navigation/task_registry.json` declares the
workflow `p-vs-np-target-navigation-run`, the composed generative skills, the
deterministic hooks, the artifacts, and the validators.

## Generative Skills

The Looper skills are judgment-heavy but bounded:

- `looper-target-goal-enricher`
- `looper-target-dependency-cartographer`
- `looper-workflow-contract-governor`
- `looper-hook-policy-maintainer`
- `looper-release-promoter`

They produce or interpret packets, dependency graphs, workflow contracts, hook
policy, and release decisions. They do not replace deterministic validation.

## Proof Gate

Run:

```bash
python agentic/scripts/agentic_check.py
```

This replays the P vs NP target-navigation slice and validates target packets,
dependency graphs, skill projections, workflow registries, workflow contracts,
gate policy, TODO evidence, hooks, skill application logs, and release reports.
