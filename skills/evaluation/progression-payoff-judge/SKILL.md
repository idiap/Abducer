---
name: progression-payoff-judge
description: Judge whether an Abducer discovery strategy is making real progress, still has payoff potential, should be adapted, or should be stopped. Use after bounded cycle windows, marathon runs, strategy pivots, contribution-monitor updates, or whenever current outputs must be evaluated against problem history, current mathematical content, future direction, and anti-drift controls.
---

# Progression Payoff Judge

## Workflow

Judge progress from evidence, not from optimism.

1. Read the target problem statement and literature evolution.
2. Read the latest discovery cycles, current physics/mathematical story, macro strategies, qualitative graph, and contribution monitor.
3. Identify the active strategy family and the exact object it is trying to move: lemma, obstruction, construction, estimate, falsifier, analogy, simulation, or paper handoff.
4. Ask what changed in the last completed window:
   - A new mathematical object was defined.
   - A previously vague dependency became a typed obligation.
   - A calculation, derivation, or falsifier became executable.
   - A route was demoted because it failed a content-specific test.
   - A contribution candidate became closer to paper packaging.
5. Decide one of: `continue`, `continue_with_adaptation`, `backtrack`, `pivot`, `handoff`, or `quarantine`.

## Judgement Standard

Progress must be content-specific. Do not count generic elaboration, repeated strategy prose, or expanding a branch queue as progress unless it changes the mathematical state.

Use these dimensions:

- `mechanistic_gain`: Did the branch explain how the relevant quantities, objects, or regimes interact?
- `technical_specificity`: Did it name definitions, assumptions, equations, estimates, algorithms, or falsifiers?
- `problem_alignment`: Did it preserve the source theory, target object, and main-problem commitments?
- `payoff_potential`: Would one or two bounded next analyses materially change route priority or contribution readiness?
- `paper_relevance`: Would the current result plausibly support a good enough paper subgoal through conceptual depth, novelty, unblocking power, applicability, and understanding gain?
- `anti_drift_control`: Are stop, pivot, and adaptation criteria stated in terms of the branch's actual mathematical content?
- `window_learning`: Did the most recent cycle window produce nonredundant learning relative to prior cycles?

## Mathematical Invariants

Preserve these invariants while judging:

- The mathematical object under study must remain named.
- Source object, target object, transfer map, and validation handoff must not silently change.
- If the branch uses a proxy, toy model, finite cutoff, analogy, or empirical support, its transfer condition must be explicit.
- Boundary regimes and edge case behavior count as evidence only when they affect the active route.

## Output Contract

Return a judgement packet with:

- `window`: cycle IDs and count judged.
- `evidence_sources`: report paths or cycle IDs used.
- `current_strategy`: concise route family and active object.
- `what_progressed`: concrete changes, each tied to evidence.
- `what_did_not_progress`: blocked or repetitive elements.
- `payoff_potential`: high, medium, watch, or low, with why.
- `decision`: continue, adapt, backtrack, pivot, handoff, or quarantine.
- `next_decisive_test`: the bounded analysis that would most change the decision.
- `when_to_stop`: content-specific stop criteria.
- `do_not_stop_prematurely_if`: content-specific reasons the branch still deserves testing.

## Epistemic Discipline

Never recommend indefinite continuation. If a branch is valuable, state the next finite test that earns more budget.

Never recommend stopping only because a problem is hard. Stop only when content-specific sharpening, validation, or source-target transfer repeatedly fails.

Never let a proxy model replace the target theory without naming the transfer certificate required to make it relevant.

State the epistemic status of the judgement: promoted, conjectural, proof-obligation, blocked, refuted, or validation-needed. Cite source artifacts, cycle IDs, KB IDs, report paths, or explicit unknowns for every major judgement.

## Failure/Demotion

Recommend demotion, quarantine, backtrack, or pivot when a branch fails a named falsifier, cannot identify its mathematical object, loses target alignment, repeats without new evidence, or cannot state a validation handoff.

Do not disconfirm a branch prematurely. A hard but essential proof-obligation remains active when it still has a bounded next action and the edge case or counterexample tests have not yet been run.
