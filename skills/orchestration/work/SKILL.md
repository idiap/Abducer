---
name: work
description: Run the persistent outer work loop that alternates discovery and prove cycles, refreshes end-to-end proof plausibility after each step, and stops either when a maximum cycle budget is reached or when the current artifacts support a plausible solution to the main problem.
---

# Work

## Conceptual Role

This is the outer control skill for the whole programme.
It alternates between:

1. `discovery`: refresh or deepen the queue of theorem-shaped proof targets;
2. `prove`: consume the next queued target and open an auditable proof attempt;
3. `proof-critic`: decide whether the current artifact chain is already a plausible end-to-end solution.
4. `meta`: auto-reflect when the cycle interval hits or when the proof queue is exhausted, so the programme records what changed in understanding rather than only what executed.

## When To Use It

Use it when the user wants one command that keeps the current problem moving without drifting into uncontrolled search.

Use it when the user asks to:

1. keep working through discovery/prove cycles;
2. alternate automatically between frontier expansion and proof work;
3. stop after a fixed number of cycles;
4. stop early if the main problem looks plausibly solved.

## Workflow

1. Load the persistent work state from `artifacts/<kb-ref>/work-state.json`.
2. Refresh the end-to-end plausibility report.
3. If the stop criteria in [references/stop-criteria.md](references/stop-criteria.md) already fire, stop.
4. Otherwise run exactly one phase:
   discovery if the next phase is discovery,
   prove if the next phase is prove.
5. After the phase, refresh the plausibility report again.
6. If the auto-meta trigger fires, generate `meta-reflection-report.*`.
7. Persist the updated work state and next phase.

Use [../kb-discovery-cycle/SKILL.md](../kb-discovery-cycle/SKILL.md) for the discovery phase semantics.
Use [../kb-prove-cycle/SKILL.md](../kb-prove-cycle/SKILL.md) for the prove phase semantics.
Use [../kb-end-to-end-proof-critic/SKILL.md](../kb-end-to-end-proof-critic/SKILL.md) for the stop rule and plausibility judgment.

Read [references/stop-criteria.md](references/stop-criteria.md) for the exact stop conditions.
Read [references/prompt-template.md](references/prompt-template.md) for the outer-loop prompt shape.

## Guardrails

- Do not continue cycling if the proof critic already marks a plausible solution.
- Do not keep proving when the discovery frontier is stale and no queue item is consumable.
- Do not claim that the main problem is plausibly solved without passing the proof-critic gates.
- Treat one invocation of `work` as one outer-loop step, not an unbounded autonomous run.
- Do not skip reflective consolidation indefinitely; when the queue exhausts or the meta interval hits, the loop should record a meta judgment.

## Deterministic Path

Use `scripts/run_work_cycle.py`.

Example:

```text
python skills/orchestration/work/scripts/run_work_cycle.py --kb kb/p-vs-np.kb.md --artifacts-dir artifacts/p-vs-np --max-cycles 6
```

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `run_work_cycle.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.

## Subgoal Control Decision

Before consuming an active proof or discovery item, inspect its `Subgoal Control Decision`. Continue only for `persist_adapt` items whose failure is still informative; route `backtrack`, `pivot`, `quarantine`, and `stop` decisions to the corresponding work-loop action instead of spending another prove/discovery cycle.

## Best Machinery Assessment

Before consuming an active proof or discovery item, inspect its `Best Machinery Assessment`: `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. Spend work budget only when the selected machinery controls the current bottleneck for the active target object. If the machinery is only analogy, endpoint notation, or proxy evidence, route it to evidence, backtrack, pivot, or quarantine instead of proof work.
