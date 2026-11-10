---
name: kb-promising-direction-assessor
description: Summarize the most promising mathematical directions from final KB artifacts, explain the content-level novelty argument of each leading route, assess the next best direction to explore, and generate a report in Markdown, LaTeX, and PDF. Use when the user asks which routes are strongest, why they are novel in mathematical content, or what should be explored next from a completed run.
---

# KB Promising Direction Assessor

## Conceptual Role

This skill turns final run artifacts into a compact research-assessment report centered on leading bridge routes, their mathematical novelty, and the next route that should be explored.

## When To Use It

Use this skill after the final pipeline artifacts exist, especially:

1. `expert-hypothesis-paper.json`
2. `hypothesis-evaluation.json`

It is appropriate when the user asks:

1. what the most promising directions are;
2. what is genuinely novel in content, not only in scoring;
3. what the next best direction to explore should be;
4. for a report artifact in `.md`, `.tex`, or `.pdf`.

## Workflow

1. Read the final expert paper and hypothesis evaluation artifacts.
2. Rank the bridge portfolio by route priority.
3. Summarize the top directions in content-first terms:
   theorem pair,
   typed bridge object,
   preserved invariant,
   missing route lemma,
   failure logic.
4. Explain novelty as mathematical-program novelty unless the artifacts already support a stronger claim.
5. Select the next best direction by preferring an adjacent high-priority route that stress-tests the same carrier in a harder regime.
6. Emit Markdown, LaTeX, and PDF outputs.

## Guardrails

- Do not claim theorem-level discovery unless the artifacts already contain validated theorem-level evidence.
- Treat `supported` hypotheses as structural/explanatory support unless the run includes real evidence.
- Explain novelty using theorem delta, carrier, invariant, and missing lemma, not just priority scores.
- Prefer route-specific mathematical language over generic comments about “interesting directions”.

## Deterministic Path

Use `scripts/generate_promising_directions_report.py`.

Example:

```text
python skills/discovery/kb-promising-direction-assessor/scripts/generate_promising_directions_report.py --artifacts-dir artifacts/p-vs-np
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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_promising_directions_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
