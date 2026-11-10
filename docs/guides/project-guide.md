<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Abducer detailed project guide

This guide preserves the detailed capabilities, examples, workflow descriptions,
integration instructions, and repository notes formerly on the root README.
Start with the [project README](../../README.md) for the concise introduction
and the [documentation index](../README.md) for the common reading structure.

Abducer is a typed, replayable research workflow for constructing, comparing, testing, and retaining abductive theories over difficult mathematical and scientific problems.

It combines a knowledge-base theorem-assistance surface with a stronger canonical discovery runtime. The latter treats discovery as controlled evolution of an epistemic state: diverse conceptual systems are generated, matured in isolated branches, evaluated without collapsing every criterion to one score, reduced into semantic events, and committed by a single atomic state writer.

## Goal

Support abductive scientific and mathematical reasoning without collapsing generated ideas, conceptual preference, executable evidence, proof status, and durable state into one undifferentiated confidence score.


## Conceptual Model

The canonical workflow is an authority-separated abductive transition system:

1. Freeze one target, run, generation, and literature basis.
2. Generate structurally different high-reward conceptual systems.
3. Mature candidates in isolated parallel branches while preserving partial failure and dissent.
4. Apply recursive reflection and material conceptual transformations.
5. Produce a blind, set-valued preference over nondominated programmes.
6. Convert validated outputs into typed consumer events and feedback edges.
7. Reduce those events into exactly one compare-and-swap state commit.
8. Schedule post-commit proof work and delayed experiment descendants without granting them theory-selection authority.

The durable state retains conceptual systems, hypotheses, literature, evidence, transformations, syntheses, branch attempts, understanding deltas, relations, stale branches, refutations, and retired routes. Negative knowledge remains part of the genealogy instead of disappearing from the next prompt.

Read the full systems formulation in the [abductive workflow paper](../publications/abductive-workflow-abstraction.pdf).

## Quick Start

Abducer requires Python 3.11 or newer and uses the committed `uv.lock` environment.

```bash
uv sync --locked
uv run python skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py --help
```

This verifies the locked environment and command surface without modifying canonical research artifacts. The default local path does not require provider credentials.

Before executing a target workflow, read the [documentation index](../README.md) and [operations runbooks](../operations/README.md). Some orchestrator modes write to canonical `artifacts/<kb-ref>/` paths and should not be used as disposable smoke tests.

## Codex and Claude Code plugin

Install the `abducer` plugin to discover the public research skills in either
host. It uses a writable Abducer checkout for canonical instructions and execution.
See the [plugin installation guide](../integrations/agent-plugins.md) for both
marketplaces, invocation examples and package maintenance.

## Current Research Loop

### KB theorem-assistance workflow

Problem knowledge is organized in `KB/*.kb.md`, with inference modes for coherence formation, explanation, deduction, abduction, conceptual conjecture, proof sketching, proof-queue construction, prove cycles, and meta-level reflection.

The `work` skill coordinates the persistent outer loop. The older abductive-loop protocol is not fully autonomous: abduction and deduction remain prompt-driven checkpoints in the current deterministic orchestrator.

### Canonical theory-first discovery workflow

The canonical runtime uses digest-bound operator requests and receipts, an executable operator registry, typed artifacts, an event-sourced epistemic ledger, Pareto scheduling, isolated branch execution, single-writer reduction, immutable commits, and replayable feedback edges.

Proof-v3 and descendant experiments are post-commit constraint lanes. Experiment evidence commissioned by theory generation `N` is aggregated through controlled worlds and becomes eligible only as a later reflection input at `N+8`.

## Named Workflow Functions

The lightweight workflows keep ordinary research controlled without automatically invoking expensive specialist work:

- **Target navigation** defines the target, dependencies, acceptance conditions, and stopping rules.
- **Discovery marathon** sustains diverse exploration across multiple cycles while retaining failures and partial progress.
- **Abducer work loop** maintains concrete proof obligations, queues, negative results, and dependency state.
- **Conceptual hypothesis exploration** turns structural failures into candidate bridges, representation changes, and new validation obligations.
- **Release promotion** decides whether validated work may change durable or official iteration state.
- **Timeline paper** converts accumulated evidence and conceptual development into a claim-bounded research narrative.
- **Yang–Mills representational dynamics** specializes the shared discovery controls for the Yang–Mills programme without weakening their authority boundaries.

Specialized named workflows activate only when their explicit conditions are satisfied:

- **Evidence-to-proof-route onramp** converts sourced mathematical material into grounded, falsification-tested proof routes.
- **Conceptual frontier deepening** performs budgeted, literature-conditioned theory formation and plural conceptual adjudication after deeper blockage.
- **Theorem proof delivery** transforms an exact theorem-shaped claim into obligations, a lemma chain, and a quality-gated proof or failure disposition.
- **Scientific contribution cultivation** determines the smallest honest contribution, its value, and whether it enables the main target or a paper.
- **Manuscript result elaboration** expands bounded result modules in an existing draft while preserving claim scope; Route-A is an optional target-specific profile.
- **Deep review and reorientation** synthesizes independent critiques into a governed repair, continuation, pivot, quarantine, or stopping decision.

Workflow handoffs transport declared artifacts, not proof or truth authority. See the [named workflow guide](../architecture/named-workflows.md) for activation rules, hooks, exit gates, and composition details.

The [essential reasoning map](../reference/essential-reasoning-types.md)
projects these workflows into a compact epistemic vocabulary—deduction,
abduction, induction, transfer, counterfactual, model reasoning, refutation,
and calibration. ERFL 0.2 expresses goals, typed claim-preserving relations,
bounded reasoning iterations, terminal conditions, and explicit workflow
switches without exposing skills. Its central invariant is relational
coherence: every transition must conserve claim or state identity, scope,
provenance, taints, ceilings, and obligations; control-flow success supplies
no scientific warrant. The [ERFL workflow representations](../reference/workflows-in-erfl.md)
show the canonical flow for every current workflow and subworkflow, together
with alias resolution and projection-confidence boundaries. The
[complete single-file ERFL listing](../reference/all-reasoning-flows.md)
contains the full source of every represented flow.

The accompanying [epistemic output typology](../reference/epistemic-output-types.md)
separates claims, evidence, decisions, models, relations, obligations, plans,
presentations, and bundles from their repository artifact materializations.

`cohere-fast` is a separate opt-in workflow for critically adapted external research methods. It is invoked explicitly as `cohere-fast <domain> [subworkflow]`; the initial route is `cohere-fast ym`. Its domain skills, runs, artifacts, hooks, and reports are isolated from existing workflows, and generic domain prompts never activate it. See the [cohere-fast workflow guide](../workflows/cohere-fast.md).

## Results Worth Inspecting

- `artifacts/<kb-ref>/`: target-scoped reasoning and proof-state artifacts.
- `phyp/`: proof-hypothesis sets and rendered companions.
- `InformalMathLib/<kb-ref>/`: persistent local and imported mathematical results used by prove cycles.
- `agentic/state/`: typed workflow and transaction state.
- `agentic/reports/`: generated inspection, validation, and publication artifacts.
- `docs/publications/`: editable LaTeX papers and rendered PDFs.

Generated `latest` reports are convenience projections unless a specific contract says otherwise. Canonical scientific authority is bound to exact target, run, generation, digest, and commit identities.

## Documentation

- [Named workflows](../architecture/named-workflows.md): conceptual guide to active and opt-in research workflows, their roles, boundaries, and handoffs.
- [Architecture](../architecture/architecture.md): system structure and component map.
- [Architecture index](../architecture/README.md): data contracts, orchestration, and publication.
- [Operations](../operations/README.md): running, observing, and troubleshooting workflows.
- [Research methods](../research-methods/README.md): epistemic, conceptual, proof, and evaluation disciplines.
- [Skill reference](../reference/skills.md): scientific skill catalog and mappings.
- [CLI reference](../reference/cli-reference.md): maintained command surfaces.
- [Publications](../publications/README.md): framework papers and formal descriptions.
- [Plans and reviews](../plans-and-reviews/README.md): mutable assessments and roadmaps.

## Project-Support Skills

Repository documentation, workflow health, architecture reporting, evolution analysis, and evidence-qualified paper production live separately in [`proj_skills/`](../../proj_skills/INDEX.md). They support project maintenance and do not participate in mathematical reasoning or replace Prism request controls.

The paper stack can index a frozen repository, derive functional/workflow/execution models, curate licensed claims, assign section writers, assemble LaTeX, and validate the resulting bundle. Repository-only runs intentionally withhold novelty, comparison, and efficacy claims.

## Repository Layout

- `skills/`: scientific and orchestration skill definitions, metadata, references, and scripts.
- `agentic/`: typed discovery runtime, schemas, registries, transactions, reports, and TODO decks.
- `proj_skills/`: project-maintenance and framework-paper skills.
- `KB/`: one structured knowledge base per problem space.
- `InformalMathLib/`: problem-scoped persistent theorem and result memory.
- `phyp/`: generated proof-hypothesis artifacts.
- `artifacts/`: target and run outputs.
- `tests/`: thematic contract, adversarial, generative, formal, domain, and orchestration coverage.
- `docs/`: reader-oriented documentation and publications.

## Development Status

The repository is a research system under active development. Core transition, receipt, reducer, persistence, proof, and delayed-experiment contracts have deterministic coverage.

Repository source headers identify the project as MIT-licensed.
