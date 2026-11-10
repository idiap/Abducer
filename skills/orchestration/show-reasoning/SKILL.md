---
name: show-reasoning
description: Display the current surfaced reasoning process as a live terminal dashboard over `artifacts/reasoning-surfaces`, with proof-discovery-language programs and material-inference operations shown directly in the UI. Use when the user asks to watch reasoning live, inspect the current epistemic state while `work` or other skills run, or render the latest reasoning state for one problem or run id.
---

# Show Reasoning

## Conceptual Role

This skill is the live observability layer for the reasoner.
It reads the surfaced reasoning channel rather than raw internal logs and renders the current epistemic process as a terminal dashboard.

The viewer prioritizes proof-discovery-language notation and the material-inference operations underneath it.

## When To Use It

Use it when:

1. `work` or another scripted stage is running and you want to inspect the current reasoning state live;
2. you want a problem-scoped view over recent surfaced moments, agents, and PDL structure;
3. you want to inspect a specific `run_id`;
4. you want the latest reasoning state rendered with LaTeX-style notation mapped into terminal math symbols.

## Workflow

1. Read surfaced reasoning JSON files from `artifacts/reasoning-surfaces/*/*.json`.
2. Filter by `kb_ref`, `run_id`, or `agent` when needed.
3. Build a current snapshot from:
   latest surfaced moments,
   active agents,
   latest PDL payload,
   material-inference operations,
   and control objects.
4. Render the snapshot as a Rich terminal dashboard.

## Guardrails

- Prefer surfaced reasoning over raw internal logs for the live dashboard.
- Treat the dashboard as an observability layer, not as proof evidence.
- If a moment lacks PDL payload, show that absence explicitly rather than inventing one.
- Prioritize the LaTeX-oriented PDL notation when available and render it into readable terminal symbols.

## Deterministic Path

Use `scripts/show_reasoning.py`.

Example:

```text
python skills/orchestration/show-reasoning/scripts/show_reasoning.py --kb-ref p-vs-np --watch
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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `show_reasoning.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: selected route, target-relevance and drift-risk evidence, skill sequence, executed commands if any, produced artifacts, unresolved obligations, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote routes that exceed budget, omit commitment citations, skip validators, or drift into low-value hypotheses.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.

## Subgoal Control Decision

When rendering active reasoning state, show each route's `Subgoal Control Decision`: decision, target-object link, blocker, learning from failure, next action, and backtrack/pivot/quarantine/stop triggers. The display should make stale persistence visible rather than hiding it behind route labels.

## Best Machinery Assessment

When rendering active reasoning state, show each route's `Best Machinery Assessment`: `machinery_role`, `controlled_interface`, `why_best_available`, `premature_use_warning`, `required_bridge_obligation`, `invalid_use_modes`, and `validation_handoff`. The report must answer why this abstraction is being used now, how it fits the target-object contract, and which premature uses are blocked.
