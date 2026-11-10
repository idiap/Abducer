<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Architecture

This is the deeper technical companion to the root `README.md`. It walks through one
`hegelian-solver run` end to end, then the schema model graph, then where the framework is
extended and where it is currently weakest. Read the README first for install/CLI/quick
start; read this for "why does the code look like this".

## One run, stage by stage

`hegelian_solver/orchestrator.py:run_solver` is the single entry point both the CLI's `run`
command and `use_cases.run_use_case_suite` call. It executes, in order:

1. **Domain profile** (`domain.py:domain_profile`) — detect `mathematical_concept` /
   `physical_concept` / `language_model_concept` / `generic_concept` and load that domain's
   failure taxonomy, discovery taxonomy, validation gates, and ranking feature names.
2. **Concept formalization** (`formalizer.py:formalize_concept`) — turn the raw input dict
   (or bare prose string) into a strict `ConceptNode`/`PhysicalConcept`/`LanguageModelConcept`,
   recording any still-missing required field as an explicit `unknown` instead of guessing.
3. **Task & evidence curation** (`evidence.py:curate_tasks_and_evidence`) — wrap
   examples/counterexamples as typed `Evidence`, and add deterministic stress tasks
   (closure, solvability, completeness, invariance, rigidity, non-collapse, residual-limit
   scan) plus domain-specific tasks on top of whatever the concept already declared.
4. **Failure classification** (`failures.py:classify_failures`) — turn counterexamples and
   reported failures/anomalies into typed `FailureCertificate`s with a taxonomy label,
   witness, failed obligation, trace, and repair-target hint.
5. **Discovery mining** (`discovery.py:mine_discovery_signals`) — detect positive structural
   pressure (shared interfaces, invariant patterns, symmetries, tool/trace usage) that isn't
   itself a failure, as typed `DiscoverySignal`s.
6. **Candidate generation** (`operators/library.py:propose_candidates`) — for every
   (failure-or-signal, operator) pair, build one `TransformationCandidate`: a target
   concept, a preservation map, a resolution mechanism, expected obligations, and seed
   ranking features.
7. **Validation** (`validators/core.py:validate_candidates`) — check every candidate's
   expected obligations and produce a `ValidationPacket` per candidate, with
   `hard_gate_failures` populated for any failed core obligation.
8. **Ranking** (`ranker.py:rank_candidates`) — hard gates first (an absolute veto), then a
   weighted score, producing one `RankingDecision` per candidate: `accept`,
   `accept_as_branch`, `provisional`, `defer`, or `reject`.
9. **Reflective refinement** — steps 6–8 repeat, bounded, against the best candidate's own
   target concept (see below), instead of stopping after one pass.
10. **Graph update** (`graph/store.py`) — every iteration's accepted/provisional candidates
    become `ConceptGraphNode`s and `ConceptGraphEdge`s; rejected candidates are kept as
    boundary evidence rather than discarded.
11. **Explanation** (`explanations.py:explain_run`) — a plain-language paragraph naming the
    move, whether it's a verified `Aufhebung` or a provisional candidate repair, and the
    residual limits.

Every stage above also has a standalone CLI subcommand (`classify-failure`, `mine-discovery`,
`propose`, `verify`, `rank`, `explain`) so it can be exercised independently of a full run —
see `cli/main.py`.

Two more artifacts are built from the same data after the loop: a `ReasoningLog`
(`reasoning_log.py`) — one `ReasoningLogStep` per stage above, each with a plain-language
narrative, a public rationale, checks, and a structured `machine_summary` — and an HTML
report (`reports/html.py`) that renders that log with a narrative line plus a formal panel
(tables, chips, obligation/ranking detail) per step, so the same run can be read either as a
story or as a spec.

## The reflective refinement loop

A single propose → validate → rank pass rarely reaches `accept`: most operators add at
least one obligation (`coverage`, `transfer`, `adequacy`, `universality`, ...) that the
deterministic validator (no proof engine behind it) can only ever mark `partial`. Stopping
after one pass would report whatever that pass produced even when a different operator
chain might do better, and would have no way to notice it had nothing left to try.

`run_solver`'s loop instead treats the **best candidate's own open obligations** as new
determinate negations of **its own target concept**, and re-proposes against it — exactly
the mechanism the solver already uses for a source concept's counterexamples, just applied
one hop further down the graph (`orchestrator._refinement_triggers`). This keeps refinement
inside the existing typed pipeline instead of bolting on an ad hoc retry mechanism.

Stopping criteria, checked in this order after every iteration
(`orchestrator._decide_stop`):

| Reason | Condition | Why stop here |
|---|---|---|
| `resolved` | best decision is `accept`/`accept_as_branch` | success — nothing left to refine |
| `no_candidates` | nothing was generated | nothing to refine |
| `no_refinement_triggers` | best candidate's open obligations map to no new trigger | another iteration would replay the same inputs |
| `plateau` | best score did not improve by more than `SCORE_IMPROVEMENT_EPS` (0.01) | this backend can't manufacture new evidence, so an unimproved score means the next iteration would reproduce the same shape of partial obligations (verified empirically: AbstractInterface/Categorify chains regenerate identical `coverage`/`transfer`/`universality` obligations every pass) |
| `max_iterations` | iteration count reached the cap (default 3, `run --max-iterations N`) | hard safety net in case the heuristics above miss a cycle |

Across the 65-case use-case suite, 22 cases resolve in one iteration and 43 plateau at two;
`no_candidates`, `no_refinement_triggers`, and `max_iterations` are exercised directly by
`tests/unit/test_orchestrator_refinement.py` rather than occurring naturally in that corpus.

External code can observe (or, by raising from a callback, interrupt) every iteration via
`hooks.SolverHooks`: `on_iteration_start`, `on_candidates_generated`, `on_validated`,
`on_ranked`, `on_iteration_end`, `on_stop`. All default to no-ops, so passing no hooks
changes nothing. The full iteration history is also recorded as a `reflective_refinement`
reasoning-log step / report panel and as `SolverTrace.refinement`.

## Mechanism reasoning (abductive layer)

Mechanism reasoning is a separate, provisional track for "how might this crisis be
addressed" questions, structured as four chained packets
(`schemas/mechanisms.py`, mirroring the `agents/hegelian-*mechanism*` skill prompts):

```
mechanism_abduction_packet        -- candidate mediating mechanisms (hypotheses), each with
                                      formal_mediation (predicates/maps/constraints) and
                                      material_mediation (actors/practices/resources)
       |
       v
mechanism_requirements_packet     -- the selected hypothesis turned into formal/material/
                                      interface/epistemic/safety/regime requirements
       |
       v
mechanism_counterfactual_critique -- remove/invert/shift/proxy-capture/... stress tests
                                      against those requirements
       |
       v
mechanism_todo_packet             -- ordered proof/evidence/design/implementation/
                                      validation/decision backlog, with stop conditions
```

`mechanisms.py:mechanism_validation_packet` is the bridge back into the main typed pipeline:
it turns a requirements packet's requirements into `Obligation`s (status `planned` unless a
counterfactual test names that requirement, in which case the test's `result` decides
`failed`/`partial`/`passed`), and turns any TODO with `blocks_candidate_acceptance: true`
into an additional hard-gate `Obligation`. The result is a normal `ValidationPacket` —
mechanism work is tracked under the same non-passing-by-default discipline as a
transformation candidate, but mechanism dossiers are **not** automatically folded into
`run_solver`'s candidate generation (see TODO.md Phase 19); today they're attached to a
report (`report --mechanisms <file>`) or inspected directly (`mechanism dossier ...`).

## Schema model graph

All public artifacts are strict Pydantic models (`extra="forbid"`) in
`schemas/models.py` (core pipeline) and `schemas/mechanisms.py` (mechanism reasoning),
re-exported together from `schemas/__init__.py`. Rough shape:

```
DomainProfile
ConceptNode --(domain subtype)--> PhysicalConcept | LanguageModelConcept
  |-- Task, Evidence
  |-- FailureCertificate, DiscoverySignal           (triggers)
        |-- TransformationCandidate                  (proposed move)
              |-- Obligation* --> ValidationPacket    (is the move justified)
              |-- RankingDecision                     (accept/branch/provisional/defer/reject)
              |-- ConceptGraphEdge (+ ConceptGraphNode for source/target)
ReasoningLog (ReasoningLogStep*) + SolverTrace         (full public record of one run)
MechanismDossier (abduction, requirements, critique, todo packets)
RunLedger (LedgerEntry*)                               (resumable per-stage payload log)
```

`schemas/json_schema.py:export_json_schemas` writes one `<Model>.schema.json` per model
under `data/schemas/` via `hegelian-solver schema`; regenerate after changing a model.

Deterministic, content-addressed ids (`ids.py:stable_id`) — never counters or random UUIDs —
mean re-running the same input always produces the same ids, which is what lets
`RunLedger.resume_payload()` exist and lets tests assert on exact id values.

## Extension points

See the README's "Extending" section for the step-by-step recipes (new domain adapter,
failure label, discovery signal, operator). The one-line summary: most extensions touch
`domain.py` (taxonomy), one of `failures.py`/`discovery.py` (detection), `operators/library.py`
(repair mapping + candidate template), and `validators/core.py` (any new hard gate) — in that
order, source to sink, matching the pipeline stage list above.

## Known representational gaps

TODO.md Phase 19 records the findings from a full workflow review in more detail; in short:

- `failures.REPAIR_TARGETS` and `operators.library.FAILURE_TO_OPERATORS` are two separately
  maintained copies of the same label → operator mapping and have already drifted.
- `DomainProfile.validation_gates` is descriptive only — `validators/core.py` hardcodes its
  own hard-gate kind set rather than reading the domain profile.
- `operators.library._ranking_features` returns fixed constants per (operator, domain), not
  values derived from how strong a given concept's own evidence is.
- `failures._label_from_text` and `domain.detect_domain`'s text fallback are first-match
  keyword search, which can misroute concepts whose free text happens to contain another
  domain's marker word.
- `TransformationCandidate.target_concept` is a renamed, re-tagged copy of the source
  concept, not a structurally new theory — representationally the weakest link at
  65-scenario scale, acceptable for demonstrating the pipeline's shape.

None of these are blocking; they're prioritized opportunities for hardening the
deterministic backend before any of it is treated as a load-bearing claim about a concept's
behavior rather than a demonstration of the pipeline's shape.
