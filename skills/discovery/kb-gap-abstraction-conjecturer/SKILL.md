---
name: kb-gap-abstraction-conjecturer
description: Given connector, pathway, bridge-plan, hardness, and phyp artifacts, investigate concept gaps and conjecture which mathematical abstraction or object types could close them. Use when the user asks for conjecture mode, concept-gap analysis, bridge-filling abstractions, missing intermediate mathematical objects, or a systematic search for abstractions that would make a proof bridge testable.
---

# KB Gap Abstraction Conjecturer


## Conceptual Role

This skill implements the conjecture mode: it studies concept gaps around promising bridges and proposes mathematical objects or abstractions that could close those gaps.

## Framework Contribution

It contributes conceptual discovery by generating bridge-filling abstraction families, definitional profiles, and counterfactual probes.

## How To Read Outputs

Read its conjectures as candidate bridge concepts with necessary and sufficient attributes; the value lies in the abstraction profile and failure analysis, not only in the label.

## Overview

Run the distinct `conjecture` inference mode.

This stage does not rank existing bridges. It asks a different question:
which mathematical abstraction, surrogate object, invariant, gadget, certificate, or representation would make an existing bridge mathematically specific enough to test?

It now also performs:

- definitional reasoning: which attributes are necessary, and which attribute bundles are sufficient, for a bridge-filling concept
- counterfactual reasoning: what happens to the bridge if those attributes are removed, weakened, or fully realized
- two-phase epistemic assessment: what constructive route the object would enable, and what impossibility or obstruction route would test or rule it out

Use it after `bridge-plan` when the current bridge web is informative but still conceptually under-specified.

For shallow, definitional, or representation-limited routes, run
`mathematical-concept-gap-revisitor` first, then audit generated abstraction
families with `abstraction-fit-gap-auditor` and state the survivor's
requirements with `efficient-representation-requirements-elicitor`.

Read [references/script-usage.md](references/script-usage.md) for the executable interface.
Read [references/prompt-template.md](references/prompt-template.md) when a narrative conjecture prompt is needed.

## Workflow

1. Load structured artifacts only: `analysis`, `entrypoints`, `pathways`, `bridges`, `phyp`, and optional `hardness`.
2. Diagnose concept gaps per bridge: model mismatch, implication lift, missing invariant, transfer mechanism, barrier pressure, regime mismatch.
3. State the declarative tension that any abstraction must resolve.
4. Conjecture abstraction families that could fill those gaps.
5. Derive necessary attributes, sufficient attribute sets, and counterfactual probes for each conjectured bridge concept.
6. Assess both constructive payoff and negative/impossibility pressure for each object hypothesis.
7. Emit human-readable construction templates, abstraction-fit handoff, efficient-representation requirements, and validation questions.

## Guardrails

- Use typed processed outputs rather than raw lexical matches over the KB body.
- Treat conjectures as bridge-repair proposals, not as accepted mathematical claims.
- Prefer abstraction families that preserve inferential identity: model, consequence, invariant, and barrier scope.
- Keep each conjecture falsifiable through explicit validation questions.
- Nothing here is purely syntactic; interpret artifacts as evidence of inferential roles and theorem-family commitments.
- Do not promote an abstraction family that cannot state what it preserves, what
  it hides, and what efficient representation requirements it must satisfy.

## Output Contract

Return:

1. `metadata`
2. `gap_clusters`
3. `abstraction_conjectures`
4. `declarative_tensions`
5. `abstraction_fit_handoff`
6. `efficient_representation_requirements`
7. `recommended_run_order`

Use `scripts/conjecture_gap_abstractions.py` for deterministic outputs.

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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `conjecture_gap_abstractions.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
