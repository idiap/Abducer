---
name: kb-orchestrator
description: Orchestrate traceable mathematical knowledge-base workflows over KB/*.kb.md. Route LaTeX ingestion, proof-graph coherence, entrypoint discovery, epistemic-hardness diagnostics, concept bridges and revisions, conjectures, proof strategies and sketches, expert papers, hypothesis evaluation and refutation, interpretation reports, and reasoning visualizations. Use when a request needs coordinated KB reasoning or selection among ingestion, explanation, deduction, abduction and bounded discovery loops. Induction is only a late-stage synthesis over existing bridge, strategy or proof artifacts.
---

# KB Orchestrator


## Conceptual Role

This skill coordinates the full KB reasoning workflow by routing intents, enforcing stage order, and preserving artifact/log consistency for each KB.

## Framework Contribution

It contributes end-to-end reproducibility and makes the multi-skill framework behave like one coherent reasoning system instead of a loose collection of scripts.

## How To Read Outputs

Read its outputs as run-level workflow summaries: they explain which inference modes were executed, which artifacts were produced, and how the reasoning state evolved.

## Overview

Route user intent to the minimum required KB skill sequence and maintain a stable KB-centric workflow.

Read [references/routing-matrix.md](references/routing-matrix.md) for routing rules.
Read [references/prompt-template.md](references/prompt-template.md) for orchestration prompts.
Read [references/abductive-loop.md](references/abductive-loop.md) for round-based loop policy.
Read [references/script-usage.md](references/script-usage.md) for executable deterministic orchestration.
Read [references/phyp-doc-export.md](references/phyp-doc-export.md) for Markdown->LaTeX/PDF export in `phyp/`.

## Orchestration Workflow

1. Detect primary intent.
Classify request into one of: `ingest`, `cohere`, `connect`, `coherence-eval`, `interpretation-reports`, `process-graph`, `reasoning-dynamics`, `entrypoints`, `hardness`, `bridge-plan`, `conceptual-revision`, `conjecture`, `strategies`, `proof-sketch`, `expert-paper`, `hypothesis-eval`, `hypothesis-loop`, `revision-loop`, `explain`, `deduce`, `abduce`, `induce`, `abductive-loop`, or `pipeline`. Reserve `induce` for local generalization over already-isolated bridge/strategy/proof families.

2. Resolve KB target.
Select or create `KB/<problem>.kb.md`. If ambiguous, infer from explicit problem title first, then dominant domain terms.

3. Build minimal execution plan.
Use only needed skills:
- `ingest` -> `latex-kb-ingest`
- `cohere` -> `kb-proof-connector` -> `kb-coherence-evaluator`
- `connect` -> `kb-proof-connector`
- `coherence-eval` -> `kb-coherence-evaluator`
- `interpretation-reports` -> `kb-orchestrator/generate_interpretation_reports.py`
- `process-graph` -> `kb-orchestrator/generate_process_graph.py`
- `reasoning-dynamics` -> `kb-orchestrator/generate_reasoning_dynamics.py`
- `entrypoints` -> `kb-entrypoint-finder` -> `kb-entrypoint-pathfinder`
- `hardness` -> `kb-epistemic-hardness`
- `bridge-plan` -> `kb-concept-bridge-planner`
- `conceptual-revision` -> `mathematical-concept-gap-revisitor` -> `abstraction-fit-gap-auditor` -> `efficient-representation-requirements-elicitor`
- `conjecture` -> `mathematical-concept-gap-revisitor` -> `kb-gap-abstraction-conjecturer` -> `abstraction-fit-gap-auditor` -> `efficient-representation-requirements-elicitor`
- `strategies` -> `kb-novel-proof-strategist`
- `proof-sketch` -> `kb-proof-sketcher`
- `expert-paper` -> `kb-expert-paper-generator`
- `hypothesis-eval` -> `kb-hypothesis-evaluator`
- `hypothesis-loop` -> `kb-hypothesis-refutation-loop`
- `revision-loop` -> `kb-revision-loop`
- `explain` -> `kb-explain`
- `deduce` -> `kb-deduce`
- `abduce` -> `kb-abduce`
- `induce` -> `kb-induce` (optional; strategy/proof domain only)
- `abductive-loop` -> `kb-proof-connector` -> `kb-coherence-evaluator` -> `kb-abduce` -> `kb-deduce` -> `kb-hypothesis-evaluator` -> `kb-hypothesis-refutation-loop` -> `mathematical-concept-gap-revisitor` when unresolved clusters are shallow or representation-limited -> `kb-revision-loop` (iterate)
- `pipeline` -> `latex-kb-ingest` -> `kb-proof-connector` -> `kb-coherence-evaluator` -> `kb-entrypoint-finder` -> `kb-entrypoint-pathfinder` -> `kb-epistemic-hardness` -> `kb-concept-bridge-planner` -> `mathematical-concept-gap-revisitor` -> `kb-gap-abstraction-conjecturer` -> `abstraction-fit-gap-auditor` -> `efficient-representation-requirements-elicitor` -> `kb-novel-proof-strategist` -> `kb-proof-sketcher` -> `kb-hypothesis-evaluator` -> `kb-hypothesis-refutation-loop` -> `kb-revision-loop` -> `kb-orchestrator/generate_process_graph.py` -> `kb-orchestrator/generate_reasoning_dynamics.py` -> `kb-expert-paper-generator`

`cohere` is the preferred inference-mode name when the user wants to build the relational bridge web and immediately evaluate global theory fit. `connect` is retained as the connector-only legacy alias.

4. Run gated transitions.
Do not proceed to a reasoning stage if ingest left unresolved structural errors (missing symbols, broken dependencies, malformed statements).

5. Persist and summarize.
When KB content changes, append a one-line note to `# Change Log` and report exact files and IDs touched.
For abductive-loop runs, also persist hypotheses under `phyp/<kb-slug>.proof-hypotheses.yaml`.
Always emit run-level reasoning-log index artifacts so logging coverage can be audited.

## Conceptual Abstraction Revision Gate

Run `conceptual-revision` before another proof-search cycle when a route is
stuck in local lemmas, reports a near-definitional transfer theorem, repeats a
fragmented proof ensemble, cannot name its conceptual tension, or has no
efficient representation requirements. The gate must produce a declarative
tension, an abstraction-fit verdict, and a representation-requirements packet.
Only then send the route to proof search, abstraction forging, literature
import, or quarantine.

## Abductive Loop Policy

For `abductive-loop` intent, run this cycle:

1. `kb-proof-connector`: rank intervention points and candidate links.
2. `kb-coherence-evaluator`: score explanatory power and global coherence deltas.
3. `kb-abduce`: generate minimal hypotheses for top-ranked points.
4. `kb-deduce`: test consequences and eliminate weak hypotheses.
5. `kb-hypothesis-evaluator`: classify each hypothesis as supported/refuted/inconclusive.
6. `kb-hypothesis-refutation-loop`: iterate unresolved hypotheses until convergence or round limit.
7. `kb-revision-loop`: produce concept/definition/regime repairs when unresolved clusters persist.
8. Repeat for up to 3 rounds or until no score improvement.

## Guardrails

- Keep provenance explicit: no reasoning claim without statement IDs.
- Treat `tentative` statements as provisional evidence.
- Prefer a short, auditable route over broad multi-skill chains.
- Treat connector link proposals as hypotheses until validated by deduction.
- Stop and surface blockers instead of inventing missing source content.

## Output Contract

For orchestrated runs, return:

1. `Intent Classification`
2. `Selected KB`
3. `Skill Route`
4. `Execution Summary`
5. `Updated IDs`
6. `Top Intervention Points`
7. `Conceptual Tension and Representation Requirements` when the route passed through `conceptual-revision`
8. `Open Risks`

Use `scripts/run_orchestrator.py` for deterministic route execution across scripted stages.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Do not let a fluent or busy workflow consume horizon budget without target relevance, evidence, and validation handoff.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: workflow route, active target ledger, skill sequence, route budget, state artifact, and candidate disposition.
- Preserved invariants: target commitments, route order, budget boundaries, evidence handoffs, and stop/quarantine conditions.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `execute_recommended_focus.py, export_phyp_docs.py, generate_concept_evolution.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
