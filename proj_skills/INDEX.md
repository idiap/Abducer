<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Abducer Project Support Skills

This pack provides repository-management support for Abducer. It is deliberately separate
from the scientific capability catalog in `skills/`: these skills maintain documentation,
inspect workflow governance, explain declared architecture, and report repository evolution.
They do not select theories, validate proofs, promote publications, or replace Prism request
planning, verification, persona review, or release gates.

## Operating Rules

- Start repository changes through `prism-spec-orchestrator` and keep `to-do.md` plus the
  active `.prism/<request>/` workspace synchronized.
- Treat audit matches and history classifications as triage signals, not established defects
  or functionality evidence.
- Prefer read-only inspection. Write only the README/report explicitly requested by the user.
- Use repository-relative paths and temporary outputs for verification.
- Distinguish declared topology, observed execution, replayed history, inference, and verified behavior.

## Project Front Door

Trigger when `README.md`, installation guidance, first-run commands, or public claim boundaries
need synchronization. Public entrypoint: `$project-readme-orchestrator`.

1. `$project-readme-concept-builder`
2. `$project-onboarding-path-verifier`
3. `$project-readme-orchestrator`

## Workflow Architecture

Trigger when a maintainer needs a readable model of the declared Prism and Abducer skill/workflow
surfaces. Public entrypoint: `$project-workflow-graph-reporter`.

1. `$workflow-contract-extractor`
2. `$workflow-graph-modeler`
3. `$workflow-graph-html-reporter`

The graph describes documentation and registry topology. It is not proof of runtime reachability.

## Workflow Governance And Health

Trigger for a periodic, advisory review of evidence boundaries, skill visibility, instruction
control, mocks/placeholders, and nearby deterministic coverage. Public entrypoint: `$workflow-health-audit-orchestrator`.

1. `$workflow-leakage-auditor`
2. `$workflow-orphan-skill-auditor`
3. `$workflow-prompt-control-auditor`
4. `$workflow-mock-behavior-auditor`
5. `$workflow-test-coverage-auditor`
6. `$workflow-health-html-reporter`

Confirm source context before changing core behavior; Prism verification remains authoritative.

## Project Evolution

Trigger for a current-state and Git-history report. Public entrypoint: `$project-evolution-timeline-reporter`.

1. `$project-state-profiler`
2. `$git-history-evolution-miner`
3. `$functionality-milestone-classifier`
4. `$evolution-figure-builder`
5. `$project-evolution-html-assembler`

Git history records repository changes, not proof that a feature worked or passed release gates.

## Framework AI Paper

Trigger when maintainers need an evidence-qualified academic description of the repository's
framework and workflow. Public entrypoint: `$framework-paper-orchestrator`.

1. `$framework-evidence-indexer`
2. `$framework-functional-modeler`
3. `$framework-workflow-modeler`
4. `$framework-execution-evidence-assessor`
5. `$framework-abstraction-synthesizer`
6. `$framework-paper-claim-curator`
7. `$framework-paper-blueprint-author`
8. `$framework-paper-abstract-writer`
9. `$framework-paper-introduction-writer`
10. `$framework-paper-related-work-writer`
11. `$framework-paper-method-writer`
12. `$framework-paper-architecture-writer`
13. `$framework-paper-implementation-writer`
14. `$framework-paper-evaluation-writer`
15. `$framework-paper-limitations-writer`
16. `$framework-paper-conclusion-writer`
17. `$framework-paper-figure-planner`
18. `$framework-paper-consistency-adjudicator`
19. `$framework-paper-latex-assembler`
20. `$framework-paper-validator`
21. `$framework-paper-orchestrator`

The stack treats declared topology, observed execution, replayed evidence, inference, and
verification as distinct evidence classes. External literature and result packets are optional,
authority-gated inputs; missing inputs produce explicit scope limits rather than fabricated claims.

## Prism Workflow Appendix

For paper appendices describing native Prism workflows, route through
`$framework-paper-orchestrator` and then:

1. `$framework-prism-workflow-extractor`: select and preserve source-backed native workflows.
2. `$framework-workflow-category-modeler`: define typed objects/arrows and scoped composition.
3. `$framework-paper-workflow-appendix-writer`: explain the model in appendix prose and LaTeX.

The current paper's named reasoning workflows are distinct from the Prism ME development
lifecycle. Select the intended source family explicitly. This optional prompt-contract lane
produces scratch fragments and sidecars; the fixed-section paper CLI does not run it.
Source syntax supports declared topology, while semantic laws and execution claims need
separate evidence. See each skill for its packet contract and worked examples.

## Dependent-Type Workflow Writing

For a representation using contexts, typing judgments and genuinely indexed families,
select `$framework-workflow-dependent-type-modeler` after the shared workflow extractor.
After claim curation and blueprint review, `$framework-paper-dependent-type-writer`
produces a formalization section or appendix with explained derivations and provenance.
A dependent pair can express that an assessment belongs to a particular claim;
its relation to native nominal records must be explicit. This lane supports manual
paper authoring and does not install a dependent type checker or extend the paper CLI.
The categorical lane remains available when requested.

## Concrete Examples in Every Workflow Appendix

`$framework-workflow-example-designer` plans one substantive, realistic case for each
workflow in the frozen paper scope. `$framework-paper-workflow-example-writer` turns
accepted plans into child fragments beside the workflow description and formal notation.
Examples show the problem, actual inputs, informative reasoning and a useful outcome;
receipts, approval gates and name-swapped generic stories do not meet that purpose.
Both category and dependent-type writers incorporate these fragments under their existing
section ownership. Illustrations are labeled honestly, and missing examples prevent a
complete-coverage claim. This remains a manual skill-authoring lane.

## Reasoning Taxonomy and Input/Output Figures

`$framework-reasoning-taxonomy-modeler` separates reasoning families, memberships,
nominal types and named operation ports using frozen evidence.
`$framework-paper-taxonomy-plotter` produces vector appendix figures with legends,
captions, coverage and provenance. Overlapping layers are not execution stages;
conceptual groups are not subtypes. Type views preserve wrappers and multi-input joins.
The existing appendix owner incorporates figures for either formal writing style.
This is an optional skill/local-renderer lane, not a new fixed-paper CLI stage.

## Core Conceptual Mechanisms in the Main Text

`$framework-core-mechanism-curator` identifies the conceptual transformations and
compositions that explain the framework, with evidence and substantive examples.
`$framework-paper-core-mechanism-writer` puts them at the center of the paper through
concise mechanism explanations and a connected argument. Introduction, method, abstract
and conclusion follow that core thesis. Workflow inventories, detailed type systems,
plots and exhaustive examples remain appendix support; a concrete case stays in the
main text. The blueprint assigns one section owner and accounts for noncentral components.
This is a manual writing lane; it does not alter the fixed paper runner.

## Skill Catalog

- [`project-readme-concept-builder`](project-readme-concept-builder/SKILL.md)
- [`project-onboarding-path-verifier`](project-onboarding-path-verifier/SKILL.md)
- [`project-readme-orchestrator`](project-readme-orchestrator/SKILL.md)
- [`workflow-contract-extractor`](workflow-contract-extractor/SKILL.md)
- [`workflow-graph-modeler`](workflow-graph-modeler/SKILL.md)
- [`workflow-graph-html-reporter`](workflow-graph-html-reporter/SKILL.md)
- [`project-workflow-graph-reporter`](project-workflow-graph-reporter/SKILL.md)
- [`workflow-leakage-auditor`](workflow-leakage-auditor/SKILL.md)
- [`workflow-orphan-skill-auditor`](workflow-orphan-skill-auditor/SKILL.md)
- [`workflow-prompt-control-auditor`](workflow-prompt-control-auditor/SKILL.md)
- [`workflow-mock-behavior-auditor`](workflow-mock-behavior-auditor/SKILL.md)
- [`workflow-test-coverage-auditor`](workflow-test-coverage-auditor/SKILL.md)
- [`workflow-health-html-reporter`](workflow-health-html-reporter/SKILL.md)
- [`workflow-health-audit-orchestrator`](workflow-health-audit-orchestrator/SKILL.md)
- [`project-state-profiler`](project-state-profiler/SKILL.md)
- [`git-history-evolution-miner`](git-history-evolution-miner/SKILL.md)
- [`functionality-milestone-classifier`](functionality-milestone-classifier/SKILL.md)
- [`evolution-figure-builder`](evolution-figure-builder/SKILL.md)
- [`project-evolution-html-assembler`](project-evolution-html-assembler/SKILL.md)
- [`project-evolution-timeline-reporter`](project-evolution-timeline-reporter/SKILL.md)
- [`framework-abstraction-synthesizer`](framework-abstraction-synthesizer/SKILL.md)
- [`framework-evidence-indexer`](framework-evidence-indexer/SKILL.md)
- [`framework-execution-evidence-assessor`](framework-execution-evidence-assessor/SKILL.md)
- [`framework-functional-modeler`](framework-functional-modeler/SKILL.md)
- [`framework-paper-abstract-writer`](framework-paper-abstract-writer/SKILL.md)
- [`framework-paper-architecture-writer`](framework-paper-architecture-writer/SKILL.md)
- [`framework-paper-blueprint-author`](framework-paper-blueprint-author/SKILL.md)
- [`framework-paper-claim-curator`](framework-paper-claim-curator/SKILL.md)
- [`framework-paper-conclusion-writer`](framework-paper-conclusion-writer/SKILL.md)
- [`framework-paper-consistency-adjudicator`](framework-paper-consistency-adjudicator/SKILL.md)
- [`framework-paper-evaluation-writer`](framework-paper-evaluation-writer/SKILL.md)
- [`framework-paper-figure-planner`](framework-paper-figure-planner/SKILL.md)
- [`framework-paper-implementation-writer`](framework-paper-implementation-writer/SKILL.md)
- [`framework-paper-introduction-writer`](framework-paper-introduction-writer/SKILL.md)
- [`framework-paper-latex-assembler`](framework-paper-latex-assembler/SKILL.md)
- [`framework-paper-limitations-writer`](framework-paper-limitations-writer/SKILL.md)
- [`framework-paper-method-writer`](framework-paper-method-writer/SKILL.md)
- [`framework-paper-orchestrator`](framework-paper-orchestrator/SKILL.md)
- [`framework-paper-related-work-writer`](framework-paper-related-work-writer/SKILL.md)
- [`framework-paper-validator`](framework-paper-validator/SKILL.md)
- [`framework-workflow-modeler`](framework-workflow-modeler/SKILL.md)

## Deferred Source Capability

`animate-workflow-runtime` was not imported. Its source depends on donor-specific live event
semantics and overlaps Abducer's reasoning-monitor surfaces. A future implementation needs a
separate contract against native `agentic/traces/` schemas; file timestamps or declared order
must never be presented as live execution.

See [PROVENANCE.md](PROVENANCE.md) for the source archive and adaptation boundary.

- [`framework-prism-workflow-extractor`](framework-prism-workflow-extractor/SKILL.md)
- [`framework-workflow-category-modeler`](framework-workflow-category-modeler/SKILL.md)
- [`framework-paper-workflow-appendix-writer`](framework-paper-workflow-appendix-writer/SKILL.md)

- [`framework-workflow-dependent-type-modeler`](framework-workflow-dependent-type-modeler/SKILL.md)
- [`framework-paper-dependent-type-writer`](framework-paper-dependent-type-writer/SKILL.md)

- [`framework-workflow-example-designer`](framework-workflow-example-designer/SKILL.md)
- [`framework-paper-workflow-example-writer`](framework-paper-workflow-example-writer/SKILL.md)

- [`framework-reasoning-taxonomy-modeler`](framework-reasoning-taxonomy-modeler/SKILL.md)
- [`framework-paper-taxonomy-plotter`](framework-paper-taxonomy-plotter/SKILL.md)

- [`framework-core-mechanism-curator`](framework-core-mechanism-curator/SKILL.md)
- [`framework-paper-core-mechanism-writer`](framework-paper-core-mechanism-writer/SKILL.md)
