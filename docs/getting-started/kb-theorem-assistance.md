<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# KB theorem assistance

This guide describes the KB theorem-assistance surface, including its pipeline
commands and artifact roles. It is one execution surface within Abducer; the
[execution-surface guide](execution-surfaces.md) explains how it relates to the
canonical theory-first discovery runtime. Run commands from the repository root.

## What This System Does

The repository ingests informal LaTeX/math text into a structured `KB/*.kb.md` file, then runs a chain of agentic skills to:

- connect statements into a relational proof graph,
- generate proof hypotheses in `phyp/`,
- score hypotheses by explanatory power and global coherence,
- rank conceptual entry points and pathways,
- articulate epistemic hardness for hard problems,
- plan concept bridges,
- conjecture bridge-filling mathematical abstractions,
- generate novelty-maximizing proof strategies,
- outline structured proof sketches for prioritized conjectures,
- evaluate and iterate hypotheses toward support/refutation outcomes,
- trigger ontology/representation revision loops when needed,
- generate human-readable interpretation reports for the reasoning/discovery process,
- generate dynamic typed process-graph replays plus reasoning-dynamics and conceptual-dynamics dashboards,
- generate run-level reasoning-log indexes for logging coverage auditability,
- generate run-level reasoning-surface indexes for human-facing conceptual dynamics,
- monitor concept/hypothesis evolution and surfaced conceptual taxonomies over a run.

## Documentation Map

The documentation is grouped by the question a reader is trying to answer. Start with
architecture for the system model, operations for running it, and research methods for the
reasoning disciplines. Case studies and publications apply those foundations to concrete work.

### Themes

- [Architecture](../architecture/README.md) — how the system and its durable artifacts fit together.
- [Reference](../reference/README.md) — exact commands, skills, protocols, and visual vocabularies.
- [Operations](../operations/README.md) — how to run, observe, and troubleshoot workflows.
- [Research methods](../research-methods/README.md) — reusable reasoning and evaluation disciplines.
- [Case studies](../case-studies/README.md) — target-scoped P-vs-NP and Yang–Mills applications.
- [Examples](../examples/README.md) — worked applications of reusable policies.
- [Integrations](../integrations/README.md) — external-system contracts, provenance, and adoption work.
- [Plans and reviews](../plans-and-reviews/README.md) — mutable roadmaps and retrospectives.
- [Publications](../publications/README.md) — source and rendered publication families.
- [Generated views](../generated/README.md) — derived, non-authoritative inspection artifacts.
- [Testing](../testing/README.md) — deterministic checks and workflow-content validation.
- [Workflows](../workflows/README.md) — runnable workflow contracts and operating examples.

## Command Template

Install the locked development environment and verify the deterministic orchestrator surface:

```bash
uv sync --locked
uv run python skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py --help
```

The command below is a maintained pipeline template, not an isolated smoke test: the current
orchestrator intentionally writes to canonical `artifacts/<kb-ref>/` paths. Review the
[orchestration contract](../architecture/orchestration.md) before running it in a working tree.

Run the deterministic pipeline:

```bash
python3 skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py \
  --intent pipeline \
  --kb KB/p-vs-np.kb.md \
  --concept artifacts/p-vs-np/concept-evolution.md \
  --rounds 3
```

Adapt an external research report into the P-vs-NP KB (replace the illustrative input path):

```bash
python3 skills/ingest/pvsnp-kb-parser/scripts/parse_report.py \
  --input /Users/user/Downloads/deep-research-report.md \
  --output-statements artifacts/p-vs-np/deep-research-report.statements.json \
  --source-id src.deep-research-report \
  --kb KB/p-vs-np.kb.md \
  --section-policy status
```

## Key Directories

- `KB/`: one knowledge-base file per problem.
- `phyp/`: proof-hypothesis YAML plus Markdown, LaTeX, and PDF publication outputs.
- `artifacts/<kb-slug>/`: structured stage outputs (JSON, Markdown, prompts).
- `artifacts/reasoning-logs/<agent-name>/`: per-run reasoning logs with step traces.
- `artifacts/reasoning-surfaces/<agent-name>/`: per-run human-facing conceptual reasoning surfaces.
- `skills/`: skill definitions, prompt templates, and scripts.
- `tests/`: contract and regression tests.

## Evidence Boundaries

- Orchestrated deterministic stages capture run identifiers and declared artifacts; this does not imply that every standalone script emits every observability surface.
- Generated hypotheses and reports are research artifacts, not proof or expert signoff.
- Tests and evaluation records provide scoped validation evidence; they do not establish theorem correctness.
- Hypothesis-loop defaults are conservative: unresolved hypotheses remain open unless stronger evidence arrives.
