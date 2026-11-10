---
name: kb-discovery-cycle
description: Run the discovery cycle that turns completed reasoning artifacts into a persistent proof queue of concrete prove-or-disprove targets. Use when the user wants to queue the next informal proof tasks, prioritize discovery outputs into a file-backed queue, or prepare theorem-pair-specific claims for later proof work.
---

# KB Discovery Cycle

## Conceptual Role

This skill converts the output of discovery-stage artifacts into a persistent queue of concrete proof targets.
Each queued item should read as a self-contained conjecture, with the route lemma recorded as the specific step to test.

## When To Use It

Use it after a KB run already produced route-level artifacts such as:

1. `expert-hypothesis-paper.json`
2. `search-space-tree.json`

Use it when the user asks to:

1. create or refresh a queue of proof targets;
2. turn promising directions into explicit prove-or-disprove tasks;
3. avoid rediscovering the same next-step proof agenda repeatedly.

## Workflow

1. Read the final bridge-first artifacts.
2. Keep only theorem-pair-specific targets with a clear claim under test.
3. State each queued item as a self-contained conjecture rather than an internal route fragment.
4. If the bridge object is still only a placeholder, escalate back to non-immediate bridge search before promoting the route.
5. If the route is shallow, definition-built, fragmented, or representation-limited, run
   `mathematical-concept-gap-revisitor`, `abstraction-fit-gap-auditor`, and
   `efficient-representation-requirements-elicitor` before a proof-queue item is promoted.
6. Preserve the missing route lemma, declared conceptual tension, abstraction-fit verdict,
   efficient-representation requirements, and supporting obligations as proof context beneath the conjecture.
7. Materialize the queue in `artifacts/<kb-ref>/proof-queue.json` and `proof-queue.md`.
8. Preserve prior queue state so completed or blocked items are not recreated as fresh work.
9. When the queue is locally exhausted, emit `discovery-breakthrough-profile.*`, `discovery-family-prompts.*`,
   `discovery-pattern-routing.*`, and `discovery-branch-queue.*` so the next discovery pass is routed by breakthrough family and epistemic pattern.
10. Materialize one dossier per routed discovery branch in `artifacts/<kb-ref>/discovery-branches/` so the search frontier becomes a persistent set of separate discovery briefs rather than only a static routing report.
11. Execute active routed branches as separate search runs when the user wants discovery to continue beyond routing; persist the resulting execution briefs in `artifacts/<kb-ref>/discovery-branch-executions/`.

Read [references/queue-policy.md](references/queue-policy.md) for prioritization rules.
Read [references/prompt-template.md](references/prompt-template.md) when a prompt-led discovery pass is needed before writing queue items.
Use [../kb-concept-bridge-planner/references/non-immediate-bridge-search.md](../kb-concept-bridge-planner/references/non-immediate-bridge-search.md) when the discovery pass cannot yet name a typed bridge object.
Use [../kb-discovery-governor/SKILL.md](../kb-discovery-governor/SKILL.md) when the question is no longer "what is the next route?" but "which routes still deserve depth at all?".
Use [../kb-discovery-breakthrough-profiler/SKILL.md](../kb-discovery-breakthrough-profiler/SKILL.md) when the frontier is blocked and discovery must first classify the kind of conceptual breakthrough or abstraction required.
Use [../../evaluation/mathematical-concept-gap-revisitor/SKILL.md](../../evaluation/mathematical-concept-gap-revisitor/SKILL.md), [../../evaluation/abstraction-fit-gap-auditor/SKILL.md](../../evaluation/abstraction-fit-gap-auditor/SKILL.md), and [../../reasoning/efficient-representation-requirements-elicitor/SKILL.md](../../reasoning/efficient-representation-requirements-elicitor/SKILL.md) when a candidate needs conceptual-abstraction revision before queue promotion.

## Guardrails

- Do not enqueue items that are only topical labels.
- Do not enqueue routes marked `re-encode-before-retrying` unless the user explicitly asks for them.
- Prefer claims that can end in either a positive or negative mathematical result.
- Keep queue items grounded in statement IDs, bridge IDs, invariants, and missing lemmas.
- Treat under-typed bridge objects as unresolved discovery work, not as mature proof tasks.
- Do not enqueue representation-limited routes unless the declarative tension,
  abstraction-fit verdict, and efficient-representation requirements are
  included as visible queue context.

## Deterministic Path

Use `scripts/enqueue_proof_candidates.py`.
Use `scripts/execute_discovery_branches.py` to consume the currently active discovery branches.

Example:

```text
python skills/discovery/kb-discovery-cycle/scripts/enqueue_proof_candidates.py --artifacts-dir artifacts/p-vs-np
python skills/discovery/kb-discovery-cycle/scripts/execute_discovery_branches.py --artifacts-dir artifacts/p-vs-np --limit 4
```

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Novelty is not value; generated hypotheses must carry status labels and disconfirming observations before receiving active attention.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: candidate bridge, conjecture, entrypoint, proof sketch, route family, or conceptual transformation.
- Preserved invariants: target commitments, source-grounded definitions, bridge compatibility, and explicit proof obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `enqueue_discovery_programmes.py, enqueue_proof_candidates.py, execute_discovery_branches.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
