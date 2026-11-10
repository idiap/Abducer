<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Test Suite Themes

The first-party test suite is grouped by the concern a test primarily protects.
Pytest still discovers every folder recursively from `tests/`, while the folders make
targeted runs and ownership clearer. Shared fixtures remain in `fixtures/`, and the
existing rubric-driven cases remain in `generative/`.

## Folder Guide

- `discovery/` covers the core theory-discovery lifecycle: candidates, conceptual
  reflection, adjudication, scheduling, canonical cycles, and publication.
- `domains/` covers domain adapters and knowledge-facing integrations, including
  literature, Category/HoTT, Yang--Mills, connectors, and physics interpretation.
- `experiments/` covers world models, experiment commissions, causal runtimes,
  descendant workers, and matched studies.
- `formal/` covers proof execution, formal claims and transformations, Lean, abstraction
  machinery, and P-vs-NP validation.
- `infrastructure/` covers schemas, contracts, dependency authority, state persistence,
  prompt contracts, and reasoning-log storage.
- `orchestration/` covers process supervision, loopers, operators, resource controls,
  workflow gates, reachability, and repository control tooling.
- `reporting/` covers human-facing reports, visualizations, monitors, graph explorers,
  and presentation artifacts.

Some integration tests cross several themes. Place a new test with the subsystem that
owns its main invariant; for example, a theory-gate test that invokes an experiment
still belongs in `discovery/` when its assertion is about promotion authority. Use an
explicit path through the `tests/` root when a test reads a module from another theme.

## Targeted Runs

Run the whole first-party suite with:

```bash
python -m pytest
```

Run one concern directly, for example:

```bash
python -m pytest tests/formal
python -m pytest tests/experiments/test_world_v3_closure.py
```

Folder placement is organizational metadata, not a marker or isolation boundary. Tests
may still use shared fixtures and production modules across the repository.
