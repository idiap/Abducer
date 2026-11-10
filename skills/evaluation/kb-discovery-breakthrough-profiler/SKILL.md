---
name: kb-discovery-breakthrough-profiler
description: Profile the conceptual breakthrough or abstraction required by the current blocked frontier. Use when the question is no longer which theorem is missing, but what kind of conceptual move discovery must make next.
---


# KB Discovery Breakthrough Profiler

## Conceptual Role

This skill sits above missing-lemma analysis.
Its job is to classify blocked routes by the kind of conceptual breakthrough they require:
realization, transport, alignment, explicitness, semantic bridging, or constructive instantiation.
It also emits broader epistemic discovery patterns such as invariant discovery, regime localization,
representation shifts, counterexample-led concept formation, route decomposition, and hybrid bridge synthesis.
It now also spawns a routed discovery layer per family and per cross-cutting pattern, so the output is not just a report
but an explicit search plan over distinct discovery branches.
Each routed layer carries a local-first heuristic for when it is worth searching externally for a mathematical framework
with similar structural properties that could serve as a foundation.

## When To Use It

Use it when:

1. the proof queue is exhausted or repeatedly blocked;
2. a prior-art pass shows that the targets are already known and the novelty locus has moved into the bridge layer;
3. discovery needs to search for a kind of abstraction rather than another theorem-shaped restatement.

## Workflow

1. Read the blocked proof frontier and the prior-art pass.
2. Group blocked routes by obstruction class.
3. For each class, determine:
   the breakthrough family,
   the abstraction required,
   the minimal theorem shape that would count as progress,
   the major-subresult type it could yield,
   and the anti-patterns that should stop discovery.
4. Rank the classes by pressure on the current programme.
5. Emit family-specific prompt packs and cross-cutting epistemic-pattern prompts.
6. Spawn routed discovery layers that alternate targeted family work with broader reframing patterns.
7. Materialize those routed layers into `discovery-branch-queue.*` plus one dossier per branch under `artifacts/<kb-ref>/discovery-branches/`.
8. Emit a dispatch order and stop criteria so discovery does not collapse into one depth-first branch.

## Guardrails

- Do not restate a missing lemma as if that were already a discovery strategy.
- Distinguish target-grounded routes from bridge-open routes.
- Prefer search instructions that produce typed objects, transfer laws, alignment theorems, or barrier theorems.
- Explicitly say what would count as superficial progress.

Read [references/prompt-template.md](references/prompt-template.md) when a prompt-led breakthrough-profiling or branch-routing pass is needed.

## Deterministic Path

Use `scripts/generate_discovery_breakthrough_profile.py`.

Example:

```text
python skills/evaluation/kb-discovery-breakthrough-profiler/scripts/generate_discovery_breakthrough_profile.py --artifacts-dir artifacts/p-vs-np
```

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_discovery_breakthrough_profile.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: objects audited, assumptions, preserved invariants, broken invariants, edge case or counterexample class, evidence paths, proof obligations, and disposition. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote on object mismatch, hidden premise shift, broken invariant, unsupported entailment, untested boundary regime, or absent witness evidence.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
