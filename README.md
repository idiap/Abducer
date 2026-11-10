<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->


# Abducer

## Overview

Abducer is a typed, replayable research system for constructing, comparing,
testing, and retaining abductive theories over difficult mathematical and scientific
problems. It preserves a problem's conceptual alternatives, evidence, failed attempts,
proof obligations, and research history rather than treating discovery as a single
answer or confidence score.

The repository has two related execution surfaces: a KB theorem-assistance workflow
and the canonical theory-first discovery runtime. The latter uses typed operator
requests and receipts, isolated branches, semantic events, and single-writer state
commits. [Getting started](docs/getting-started/README.md) explains which surface to use.

## Key concepts

- **Persistent epistemic state:** retain hypotheses, literature, conceptual systems, transformations, failures, and learned results.
- **Plural conceptual exploration:** mature structurally different candidates and preserve dissent and partial failure.
- **Separate authorities:** conceptual preference, executable evidence, proof status, publication, and durable state mutation have different contracts.
- **Replayable transitions:** bind requests, receipts, outputs, and commits to exact target, run, generation, and digest identities.
- **Governed continuation:** use obligations, budgets, stopping rules, and reflection to determine what may happen next.

## Getting started

Use Python 3.11 or newer and the committed `uv.lock` environment:

```bash
uv sync --locked
uv run python skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py --help
uv run python agentic/scripts/run_canonical_discovery_cycle.py --help
```

These commands inspect both execution surfaces without launching a research run.
The default local path does not require provider credentials. Read the
[first-use guide](docs/getting-started/README.md) before selecting a target: some
commands intentionally write canonical target state and are unsuitable as disposable
smoke tests.

## Examples

For theorem assistance, a problem such as P vs NP is represented in `KB/*.kb.md`;
skills connect statements, form and evaluate hypotheses, and maintain proof obligations.
For theory-first discovery, a cycle consumes an exact request and validated operator
receipts before reducing semantic events into one state commit.

The [detailed project guide](docs/guides/project-guide.md) preserves the conceptual
cycle, named workflow functions, and result locations. The
[named workflow guide](docs/architecture/named-workflows.md) explains activation,
composition, stopping rules, and handoffs. [Case studies](docs/case-studies/README.md)
show target-specific applications and their claim boundaries.

## Architecture

```text
problem and literature → conceptual branches → critique and typed evidence
                       → semantic reduction → atomic epistemic-state commit
                       → post-commit proof and delayed experiment work
```

`agentic/` contains the typed discovery runtime and state; `skills/` holds scientific
skills; `KB/` grounds targets; `InformalMathLib/` retains mathematical memory;
`phyp/` publishes proof hypotheses; `artifacts/` holds target outputs.
`proj_skills/` and `prism_me/` support repository maintenance and request controls.

See the [architecture overview](docs/architecture/README.md),
[data contracts](docs/architecture/data-contracts.md), and
[research methods](docs/research-methods/README.md).

## Documentation

<a id="kb-theorem-assistance-workflow"></a>
<a id="canonical-theory-first-discovery-workflow"></a>
<a id="goal"></a>
<a id="conceptual-model"></a>
<a id="quick-start"></a>
<a id="codex-and-claude-code-plugin"></a>
<a id="current-research-loop"></a>
<a id="named-workflow-functions"></a>
<a id="results-worth-inspecting"></a>
<a id="project-support-skills"></a>
<a id="repository-layout"></a>
<a id="development-status"></a>

Start with the [documentation index](docs/README.md). All project documentation
uses the same reading areas; specialist collections retain their stable paths.

- [Getting started](docs/getting-started/README.md) — Install the environment and complete a first example.
- [Concepts](docs/concepts/README.md) — Understand the project model, terminology, and evidence boundaries.
- [Guides](docs/guides/README.md) — Carry out tasks and interpret their outputs.
- [Architecture](docs/architecture/README.md) — Understand components, data flow, contracts, and extension points.
- [Reference](docs/reference/README.md) — Look up commands, skills, workflows, and documentation sources.
- [Development](docs/development/README.md) — Change the project and run the relevant checks.
- [Operations](docs/operations/README.md) — Configure, run, observe, and release maintained workflows.
- [Governance](docs/governance/README.md) — Check licensing, provenance, review, and publication requirements.
- [Archive](docs/archive/README.md) — Find historical material and distinguish plans from current behavior.

## Development and validation

Start with [AGENTS.md](AGENTS.md) and its Prism ME request controls. Documentation,
workflow health, architecture reporting, and framework-paper support remain separate
from mathematical reasoning. See [development](docs/development/README.md).

```bash
uv run pytest -q tests/infrastructure/test_documentation_layout.py
```

Use [testing guidance](docs/testing/README.md) and the affected runtime's focused
contract, adversarial, and integration tests for behavioral changes. Passing tests
provide scoped implementation evidence rather than theorem correctness.

## Limitations and status

This is a research system under active development. Generated hypotheses, conceptual
preference, rendered reports, and workflow completion do not establish mathematical
truth. The older deterministic abductive loop still has prompt-driven checkpoints.
`latest` reports are convenience projections; scientific authority remains bound to
exact artifacts and state identities. Proof and descendant experiments have their
own post-commit authority and eligibility rules.

## Dependencies and license

Repository source headers identify first-party code as MIT licensed. See
[LICENSES](LICENSES/), [REUSE.toml](REUSE.toml), [DEPENDENCIES.md](DEPENDENCIES.md),
and [software disclosure](docs/operations/software-disclosure.md) for source,
dependency, attribution, and disclosure boundaries.
