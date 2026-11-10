<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dependency Discipline

Use this guide when the request needs a dependency picture that can later be translated into real Prism onboarding work.

In Prism, dependency management is not only a package-install concern. It is a typed operational surface that spans environment bundles, preserved runtimes, reference knowledge bases, backend profiles, workspace mounts, and the file or route surfaces that a capability actually depends on.

## Goal

Build a dependency map that answers three questions clearly:

1. What does this capability depend on?
2. How is that dependency managed in Prism terms?
3. How do we verify that the dependency is present, correct, and visible to later agents?

## Prism Dependency Surfaces

Treat these as the main dependency classes.

### 1. `uv` Bundles

Prism manages Python dependency bundles through stable bundle records such as:

- `bundle_id`
- `install_kind`
- `relative_path`
- `editable_extras`
- `tags`

These represent installable environment units, not vague package piles.

Useful discovery commands:

```bash
python -m uv run prism uv status
python -m uv run prism uv sync --all --dry-run
```

Use them to see the current bundle picture and the planned install commands.

### 2. Runtime Dependencies

These are the concrete libraries, executables, models, services, files, or requirements files the capability needs at runtime.

Examples:

- Python requirements files
- editable local packages
- CLI tools
- model checkpoints
- environment variables
- remote APIs

### 3. Reference Knowledge Bases

Prism reference KBs carry more than a path. They include:

- `kb_id`
- semantic placement
- `runtime_dependencies`
- linked backends
- bootstrap steps
- availability checks

If a capability depends on a preserved corpus, theorem library, documentation index, dataset, or local index artifact, record it as a reference-KB-style dependency rather than burying it inside prose.

### 4. Backend Profiles

Imported and external capabilities often depend on explicit backend identities such as:

- LLM backends
- theorem provers
- script runners
- library indexes
- hybrid workflows

Map the backend identity, target, invocation hint, and which capability or test surface depends on it.

### 5. Runtime Adapter Surfaces

Prism treats runtime adapters as dependency-bearing structures.

Map at least:

- `workspace_mounts`
- `route_registry_path`
- `capability_source_paths`
- preserved runtime roots
- writable versus read-only surfaces

If the capability only works because a workspace has a very specific directory shape, that is a dependency and must be recorded.

### 6. Dependency Edges Across Work

Also map how dependencies affect:

- slice order
- test setup
- documentation examples
- release gates
- handoff and onboarding

This keeps the dependency map useful after planning starts.

## Mapping Procedure

1. Inventory dependencies from code, docs, scripts, tests, config, and preserved runtimes.
2. Normalize each dependency into a Prism-facing class: `uv` bundle, runtime dependency, reference KB, backend profile, runtime adapter surface, or dependency edge.
3. Mark whether the dependency is `existing`, `reused`, `new`, `proposed`, or `external-only`.
4. Mark whether the dependency is `declared`, `inferred`, or `hidden`.
5. Record the consumer: capability, slice, test, doc, or runtime adapter that depends on it.
6. Record evidence: path, command, config field, or source artifact.
7. Record verification: status command, dry run, availability check, smoke test, or manual check.
8. Record the onboarding implication: bundle id, backend profile, KB id, mount requirement, or preserved asset that later Prism import work must keep visible.

## What Good Looks Like

A strong dependency map makes it easy for another agent to see:

- which dependencies are already managed cleanly
- which ones need a Prism bundle or adapter later
- which ones are risky, hidden, or under-verified
- which slices and tests will fail if setup is wrong

## Guardrails

- Do not reduce the map to a requirements list.
- Do not hide workspace shape assumptions, KB availability, or backend choices inside narrative notes.
- Do not flatten preserved upstream runtimes into fake native Prism structure.
- Keep declared facts separate from inference.
- Treat hidden or manual-only dependencies as release risks until they are named and checked.

## Output Contract

The dependency map should make explicit:

- Prism bundle alignment
- runtime dependency inventory
- reference KB and backend mapping
- runtime adapter and workspace-mount mapping
- dependency edges into slices, tests, docs, and handoff
- hidden dependency risks
- verification commands and checks
