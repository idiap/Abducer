<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hegelian Solver

Hegelian Solver is a typed, graph-building prototype for dialectical concept development.
It turns a seed concept into structured tasks, evidence, determinate failures, discovery
signals, candidate transformations, validation obligations, ranked decisions, graph edges,
and concise explanations.

The implementation follows the references in `refs/` and the granular agent skills in
`agents/`. Hegelian terms are treated operationally:

- `Concept`: a structured theory, physical model, language-model system, or generic interface.
- `Determinate negation`: a typed failure certificate with witness, failed obligation, trace,
  repair target, and severity.
- `Discovery signal`: pattern pressure from examples, invariants, proof compression, anomaly
  clusters, latent ontology, or system traces.
- `Aufhebung`: a verified transformation that preserves predecessor structure, resolves or
  relocates the trigger, and avoids collapse.

## Install

```bash
uv sync --extra dev
```

The runtime dependencies are intentionally small: Pydantic for artifact schemas and PyYAML for
fixtures and human-authored graph files.

## Input Modes

The solver can start from several kinds of material:

- structured concept YAML/JSON;
- prose concept sketches;
- field tensions that need explicit crisis formalization;
- retrospective evolutionary narratives (prose already supplied);
- area/topic names that need a conceptual trace researched from scratch, not just formalized;
- example, counterexample, measurement, proof, benchmark, or trace bundles;
- explicit failures, discovery signals, candidates, validation packets, graphs, or reasoning logs;
- source-sensitive historical or current claims that may need web expansion.

Retrospective inputs are treated as historical reconstruction work: the input is segmented into
stages, transition pressures, preservation maps, material evidence, and epistemic limits before
the ordinary solver loop runs. When the user names only an area or topic — not prose to
formalize — `hegelian-area-concept-trace-builder` runs first: it scopes the area, identifies the
conceptual turning points worth tracing, drafts an informal natural-language account of each from
existing knowledge, and triages individual claims for targeted web search (rather than searching
the whole topic broadly) using `hegelian-web-expansion-scout`'s required/recommended/not_needed
rubric. Its informal `area_conceptual_trace` output is the recommended input to
`hegelian-retrospective-evolution-formalizer` when the user also wants formal stages and graph
seeds. `hegelian-web-expansion-scout` itself decides whether external search is required,
recommended, unnecessary, or forbidden for any claim, then turns found sources into bounded
evidence records for the flow.

Field-tension inputs are treated as crisis-formalization work: the solver elicits the opposed
commitments, maps decisive evidence and failed mediations, then emits a `tension_formalization_packet`
with the exact crisis statement, minimal incompatible commitments, material conditions, and downstream
failure/discovery hooks.

When the next question is how a formalized crisis could be addressed, the solver treats mechanism
reasoning as a provisional abductive layer. It emits mechanism hypotheses, formal and material
requirements, counterfactual critiques, and concrete TODOs before any mechanism is allowed to become
a validated transformation. Mechanism packets are typed Pydantic schemas
(`hegelian_solver/schemas/mechanisms.py`); `hegelian_solver/mechanisms.py` can turn a mechanism's
requirements (optionally enriched by its counterfactual critique and TODO backlog) into the same
`ValidationPacket`/hard-gate shape used for transformation candidates, so mechanism work is tracked
under the same non-passing-by-default discipline before it is ever proposed as a graph edge.

## Reflective Refinement Loop

A single propose -> validate -> rank pass rarely reaches a clean `accept`, since most operators add
at least one obligation (`coverage`, `transfer`, `adequacy`, `universality`, ...) that the
deterministic validator can only ever mark `partial`. `orchestrator.run_solver` therefore loops:
each iteration treats the best candidate's own *open* obligations as new determinate negations of
its target concept and re-proposes against it — the same mechanism the solver already uses for a
source concept's counterexamples, just applied one hop further down the graph. The loop stops on
whichever of these fires first:

- `resolved` — the best decision reached `accept` or `accept_as_branch`;
- `no_candidates` — nothing was generated, so there is nothing to refine;
- `no_refinement_triggers` — the best candidate's open obligations don't map to a new failure label;
- `plateau` — the best score did not improve versus the previous iteration (this deterministic
  backend cannot manufacture new evidence, so an unimproved score means the next iteration would
  just reproduce the same shape of partial obligations);
- `max_iterations` — a hard safety net (default 3, override with `run --max-iterations N`).

Each iteration fires `SolverHooks` callbacks (`hegelian_solver/hooks.py`:
`on_iteration_start`/`on_candidates_generated`/`on_validated`/`on_ranked`/`on_iteration_end`/
`on_stop`) so external code can observe or react without editing the orchestrator, and the full
iteration history is recorded as a `reflective_refinement` reasoning-log step and a dedicated panel
in the HTML report. See the `orchestrator.py` module docstring for the full stopping-criteria
rationale, and `TODO.md` Phase 19 for known representation gaps this review surfaced.

## Conceptual Creativity Analysis

Every candidate gets a typed `ConceptualCreativityAnalysis`
(`hegelian_solver/schemas/creativity.py`, built deterministically by
`hegelian_solver/creativity.py`) that answers one question explicitly: is this move creative,
or does it only restore what its trigger broke? A candidate whose `expected_obligations` are
exactly the four core ones (preservation, resolution, non-collapse, residual-limit reporting)
is classified `repair`; one that adds further obligations is `affordance_creation` (or `mixed`
for operations that read more as guardrails than expansions — quotienting, regime restriction,
governance scaffolding).

Every operator in `operators.library.ALL_OPERATOR_NAMES` is classified into one of nine
conceptual operations, so creativity is comparable across domains:

`closure_completion`, `abstraction_interface_discovery`, `invariance_reparameterization`,
`quotienting_redundancy_removal`, `localization_regime_restriction`, `externalization_or_tooling`,
`bridge_mediation`, `latent_carrier_introduction`, `governance_safety_scaffold`.

Nothing in the analysis is asserted free-form: `source_pressure`, `operation`, `new_affordance`,
`preservation_under_transformation`, `creative_risks`, and `downstream_concept_seeds` are all
required-explicit fields (`validate_creativity_analysis`), and any gap the trace artifacts can't
ground gets recorded in `residual_todos` instead of being papered over. The agent-facing version
of the same discipline is `agents/hegelian-conceptual-creativity-reasoner`. Reports render a
dedicated "Conceptual Creativity Analysis" section — readable prose first, full structured payload
collapsible — positioned before "Concrete Concept Evolution" and "Formal Reasoning Notation".

## Quick Start

Run the full solver on the number-system fixture:

```bash
uv run hegelian-solver run hegelian_solver/examples/naturals.yaml --output-dir data --human
```

Inspect the emitted graph:

```bash
uv run hegelian-solver graph inspect data/graphs/<run-id>.json
```

Render or inspect the public reasoning artifacts:

```bash
uv run hegelian-solver reasoning-log data/traces/<run-id>.json
uv run hegelian-solver report data/traces/<run-id>.json --output data/reports/<run-id>.html
```

Export JSON Schema for all public artifacts:

```bash
uv run hegelian-solver schema data/schemas
```

Run tests:

```bash
uv run --extra dev pytest
```

Run the spec-instantiated use-case suite:

```bash
uv run hegelian-solver validate-use-cases
uv run hegelian-solver run-suite --output-dir data/use_case_runs
```

## CLI Commands

- `hegelian-solver run <concept-file>` executes the full orchestrated pass.
- `hegelian-solver classify-failure <concept-file>` emits failure certificates.
- `hegelian-solver mine-discovery <concept-file>` emits discovery signals.
- `hegelian-solver propose <concept-file> <triggers-file>` emits transformation candidates.
- `hegelian-solver verify <concept-file> <candidates-file>` emits validation packets.
- `hegelian-solver rank <candidates-file> <validation-file>` emits ranking decisions.
- `hegelian-solver explain <trace-file>` prints the run explanation.
- `hegelian-solver reasoning-log <trace-or-log-file>` emits the public reasoning log.
- `hegelian-solver creativity <trace-or-log-file> [--validate]` prints conceptual creativity
  analyses, or checks them against the required-explicit-fields validation criteria.
- `hegelian-solver report <trace-or-log-file> --output <report.html>` renders the HTML report.
- `hegelian-solver graph inspect <graph-file>` summarizes graph state.
- `hegelian-solver graph export <graph-file>` emits the full graph JSON.
- `hegelian-solver schema <output-dir>` writes JSON Schema files.
- `hegelian-solver list-use-cases` lists the spec-instantiated corpus.
- `hegelian-solver validate-use-cases` checks formal/material/epistemic reasoning blocks.
- `hegelian-solver run-suite` executes the corpus and writes a machine-readable suite summary.
- `hegelian-solver run <concept-file> --max-iterations N` caps the reflective refinement loop.
- `hegelian-solver mechanism abduce|requirements|critique|todos <packet-file>` validates one
  mechanism-reasoning packet.
- `hegelian-solver mechanism dossier <file> [--id ID] [--validation-packet]` inspects a full
  mechanism dossier, or prints the `ValidationPacket` linked from its requirements/critique/TODOs.
- `hegelian-solver mechanism validation-packet <requirements-file> [--critique-file] [--todos-file]`
  builds a `ValidationPacket` directly from mechanism packets.
- `hegelian-solver report <file> --mechanisms <mechanism-examples-file>` attaches mechanism
  dossiers to the HTML report's dedicated mechanism section.

## Package Layout

- `hegelian_solver/schemas/`: Pydantic models and JSON Schema export.
- `hegelian_solver/domain.py`: math, physics, language-model, and generic domain profiles.
- `hegelian_solver/formalizer.py`: raw YAML/JSON/prose dictionary to concept node.
- `hegelian_solver/evidence.py`: task and evidence packet generation.
- `hegelian_solver/failures.py`: determinate-negation classification.
- `hegelian_solver/discovery.py`: discovery-signal mining.
- `hegelian_solver/creativity.py`: conceptual-operation taxonomy and grounded creativity analysis.
- `hegelian_solver/operators/`: transformation candidate templates.
- `hegelian_solver/validators/`: obligation generation and hard gates.
- `hegelian_solver/validators/backends.py`: registry for proof, SMT, model-finder,
  theorem-prover, simulation, benchmark, and review backends.
- `hegelian_solver/ranker.py`: multi-objective scoring and branching decisions.
- `hegelian_solver/graph/`: concept graph storage, edge construction, and queries.
- `hegelian_solver/explanations.py`: dialectical explanations grounded in artifacts.
- `hegelian_solver/reasoning_log.py`: public human/machine-readable reasoning log builder.
- `hegelian_solver/reports/`: HTML report rendering from reasoning logs (narrative + formal
  panels per stage, plus a dedicated mechanism-dossier section).
- `hegelian_solver/mechanisms.py`: mechanism dossier loaders and the bridge from mechanism
  requirements/critique/TODOs to a `ValidationPacket`.
- `hegelian_solver/hooks.py`: `SolverHooks` lifecycle callbacks for the refinement loop.
- `hegelian_solver/orchestrator.py`: full deterministic solver run, including the bounded
  reflective refinement loop (see "Reflective Refinement Loop" above).
- `hegelian_solver/use_cases.py`: spec corpus loader, validator, and suite runner.
- `hegelian_solver/cli/`: command line entrypoint.
- `hegelian_solver/examples/`: runnable YAML fixtures.

## Agent Skills

The `agents/` pack includes the core solver skills plus specialized intake, crisis-formalization,
and mechanism-abduction skills:

- `hegelian-input-typology`: classifies input kind, temporal scope, evidence state, and route.
- `hegelian-field-tension-elicitor`: surfaces opposed commitments, stakes, and pressure points.
- `hegelian-tension-evidence-cartographer`: maps decisive claims, evidence states, and failed mediations.
- `hegelian-conceptual-crisis-formalizer`: emits the exact formal crisis packet for a field tension.
- `hegelian-abductive-mechanism-hypothesizer`: infers hypothetical mediators required by a crisis.
- `hegelian-mechanism-requirements-formalizer`: turns mechanism hypotheses into testable requirements.
- `hegelian-mechanism-counterfactual-critic`: stress-tests requirements with counterfactual and adversarial probes.
- `hegelian-mechanism-todo-elicitor`: converts remaining proof, evidence, design, and validation work into TODOs.
- `hegelian-retrospective-evolution-formalizer`: turns historical prose into stages, transitions, and graph seeds.
- `hegelian-area-concept-trace-builder`: researches and writes an informal conceptual trace of an
  area's key concepts from a topic name, triaging individual claims for targeted web search instead
  of supplying prose itself.
- `hegelian-web-expansion-scout`: decides when web search is needed and integrates source evidence.
- `hegelian-use-case-motivation-writer`: explains why a use case matters before formal notation.
- `hegelian-conceptual-creativity-reasoner`: classifies each candidate's conceptual operation and
  separates repair from genuine affordance creation (see "Conceptual Creativity Analysis" above).
- `hegelian-full-explanation-builder`: expands the compact run summary into the full reader-facing
  explanation (big picture, what breaks, why this successor, what is preserved, how it was checked).

## Artifacts

The canonical artifact directories are:

- `data/concepts/`
- `data/traces/`
- `data/graphs/`
- `data/candidates/`
- `data/certificates/`
- `data/run_ledgers/`
- `data/reasoning_logs/`
- `data/reports/`
- `data/schemas/`
- `data/use_case_runs/`

Generated run traces, graphs, candidates, and certificates are ignored by Git. Exported schema
files in `data/schemas/` are kept as public contract artifacts. Run ledgers capture every
stage payload and expose a simple resume payload for future continuation tooling.
Reasoning logs record public stage-by-stage rationale, checks, decisions, assumptions, and
unknowns; HTML reports embed that same JSON for machine interpretation.

## Examples

Fixture concepts cover the initial benchmark traces:

- `naturals.yaml`: `Naturals -> Integers` style closure pressure via `GroupCompletion`.
- `metric_space.yaml`: abstraction pressure from metric spaces to open-set structure.
- `newtonian_mechanics.yaml`: physics validation with regime, measurement, and limiting-case checks.
- `assistant.yaml`: language-model no-provenance pressure mapping to retrieval/verification.
- `group_examples.yaml`: discovery of a shared interface across group-like examples.

The expanded corpus lives at `hegelian_solver/examples/use_cases/spec_use_cases.yaml`.
It instantiates 65 mathematical, physical, and language-model evolution cases from the
spec references. Every case includes formal analysis, material analysis, and an
epistemic profile so the reasoning log can distinguish structural obligations from
evidence, assumptions, uncertainty, and residual limits.

Realistic field-tension examples live at
`hegelian_solver/examples/tensions/realistic_tension_formalizations.yaml`. They cover
clinical AI, low-carbon grid planning, agentic AI governance, and urban housing policy.

Abductive mechanism examples live at
`hegelian_solver/examples/mechanisms/abductive_mechanism_requirements.yaml`. They show how
formalized crises become provisional mechanism hypotheses, requirements, counterfactual tests,
and implementation/validation TODOs.

An area conceptual trace example lives at
`hegelian_solver/examples/area_traces/cancer_mechanisms_and_therapeutics.yaml`, built with
`hegelian-area-concept-trace-builder`. It traces 11 conceptual turning points in cancer
mechanism understanding — from 19th-century tissue-level disease models through oncogenes,
tumor suppressors, multistep progression, angiogenesis dependence, the Hallmarks-of-Cancer
framework, molecularly targeted therapy, immune checkpoint discovery, the genomic-landscape
era, and CAR-T cell therapy — each paired with the therapeutic intervention its mechanistic
shift made conceivable, with per-claim web-search triage (some dates verified via targeted
search, others left at their honest confidence level rather than searched indiscriminately).

## Extending

To add a domain adapter:

1. Add labels and gates in `hegelian_solver/domain.py`.
2. Add schema fields in `hegelian_solver/schemas/models.py` if the domain needs a subtype.
3. Add domain tasks in `hegelian_solver/evidence.py`.
4. Add validators in `hegelian_solver/validators/core.py`.
5. Add ranking features in `hegelian_solver/ranker.py`.

To add a failure label or discovery signal:

1. Add the label taxonomy in `domain.py`.
2. Add classification or mining heuristics in `failures.py` or `discovery.py`.
3. Map it to an operator in `operators/library.py`.
4. Add fixture coverage and tests.

To add an operator:

1. Add the operator name and trigger mapping in `operators/library.py`.
2. Define its relation, target naming, expected obligations, and ranking features.
3. Add validators for any new hard gates.
4. Add a regression test for accepted, provisional, or rejected behavior.

## Integration Roadmap

The current implementation is deterministic and local. Natural next integrations are:

- theorem prover hooks for preservation, universality, and non-collapse proofs;
- SMT/model-finder backends for bounded counterexamples and consistency checks;
- CAS hooks for algebraic examples and completions;
- simulation and benchmark runners for physics examples;
- retrieval, tool-call replay, and red-team benchmark runners for language-model systems;
- a graph UI for browsing branches, residual limits, and rejected candidates.

## Further Documentation

- `docs/ARCHITECTURE.md` walks through the full pipeline stage by stage (including the
  reflective refinement loop) and the schema model graph, for readers who want the deeper
  technical picture rather than this file's quick reference.
- `TODO.md` is the living project log: completed phases plus, in Phase 19, a full workflow
  review with concrete, file-pointed findings about where the deterministic backend's
  representation is shallow (label classification, ranking features, hardcoded validation
  gates) and what would need to change to harden it.
