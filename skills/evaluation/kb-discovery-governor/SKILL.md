---
name: kb-discovery-governor
description: Govern mathematical discovery so search does not drift into unbounded depth-first exploration. Use when the user asks which routes deserve deeper investment, which subresults would already count as major contributions, or how to score the value of conjectures objectively from current artifacts.
---

# KB Discovery Governor

## Conceptual Role

This skill is the epistemic control layer for discovery.
It does not try to prove the main conjecture directly.
It decides which routes deserve deeper search, which routes should be lateralized or frozen, and which partial results already qualify as major contributions even without solving the main problem.

## When To Use It

Use this skill when the current artifact set already contains route-level outputs such as:

1. `search-space-tree.json`
2. `expert-hypothesis-paper.json`
3. `proof-sketches.json`
4. `proof-queue.json`
5. `hypothesis-evaluation.json`

Use it when the user asks:

1. whether discovery is drifting into an indeterminate depth-first search;
2. which subresults would already be publishable or major;
3. what makes a conjecture valuable in an objective way;
4. whether to deepen, broaden, freeze, or queue a route next.

## Workflow

1. Build the active route frontier from current artifacts.
2. Diagnose drift using explicit signals:
   repeated abstraction,
   under-typed carrier,
   no theorem-body gain,
   no new route lemma,
   repeated revisits to the same search branch.
3. Classify possible subresults as:
   standalone theorem,
   barrier or impossibility result,
   transfer principle,
   bridge object/tool,
   exploratory conjecture only.
4. Apply the major-contribution criteria.
5. Apply the conjecture-value rubric.
6. Decide for each route:
   deepen,
   lateralize,
   freeze,
   queue for proof,
   or mark as a major subresult candidate.

Read [references/governance-criteria.md](references/governance-criteria.md) for anti-drift rules and major-subresult criteria.
Read [references/conjecture-value-rubric.md](references/conjecture-value-rubric.md) for the objective scoring model.
Read [references/prompt-template.md](references/prompt-template.md) for the prompt shape that applies the framework to current artifacts.

## Guardrails

- Do not reward depth for its own sake.
- Do not deepen a route that has added no typed object, no sharper lemma, and no new falsification path.
- Count negative results as major only when they close a meaningful family of routes, not when they merely fail locally.
- Treat standalone subresults as first-class outcomes.
- Prefer routes that compress the search space, sharpen the frontier, or yield independent mathematics.

## Output Contract

Return:

1. `Drift Diagnosis`
2. `Search Allocation Decision`
3. `Major Subresult Candidates`
4. `Conjecture Value Table`
5. `Recommended Next Actions`

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- A score or label is never enough; evaluation must expose what would falsify, demote, or repair the route.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: definitions, bridge objects, candidate hypotheses, entailment gaps, premises, regimes, counterexamples, and proof obligations.
- Preserved invariants: objects compared, assumptions used, preserved invariants, broken invariants, boundary regimes, and witness evidence.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_discovery_governor_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
