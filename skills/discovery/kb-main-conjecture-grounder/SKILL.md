---
name: kb-main-conjecture-grounder
description: Ground current KB artifacts in the central theorem or conjecture under study and explain, in mathematical narrative form, how the active routes bear on that conjecture. Use when the user asks how the current bridges, proof sketches, or queue relate to the main conjecture itself, for example how a route in the P vs NP workspace bears on the claim P != NP.
---

# KB Main Conjecture Grounder

## Conceptual Role

This skill turns a route-level artifact set into a conjecture-centered argument. It explains not only what the current bridge program is, but why that program is relevant to the main mathematical claim.

## Use It When

Use it when the user asks for:

1. grounding of current artifacts in the main conjecture;
2. a logical implication chain from a route payoff to the central claim;
3. a narrative distinction between direct proof, stronger conditional target, and current frontier.

## Workflow

1. Identify the main conjecture explicitly.
2. Pull the local KB statements that define the ambient classes, target consequences, and known implication targets.
3. State the implication chain from the current leading route to the main conjecture.
4. Separate:
   direct proof content,
   stronger conditional consequence,
   unresolved route lemma,
   proof frontier.
5. Write the result as a mathematical narrative, not as a pipeline changelog.

Read [references/prompt-template.md](references/prompt-template.md) when writing the grounded narrative by hand.

## Guardrails

- Do not present a stronger consequence as if it were already proved.
- Distinguish theorem-level grounding from programmatic route-level grounding.
- Make the implication to the main conjecture explicit.
- Keep the narrative mathematical: theorem pair, carrier, invariant, route lemma, obstruction, frontier.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run deterministic validators or repository scripts only when they directly ground the current request; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
