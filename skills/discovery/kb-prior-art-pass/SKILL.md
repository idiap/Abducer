---
name: kb-prior-art-pass
description: Run a targeted prior-art / InformalMathLib pass over blocked routes or missing lemmas, import decisive external theorem references into InformalMathLib, and generate a content-first report of what the literature changes about the current proof state.
---


# KB Prior-Art Pass

## Conceptual Role

This skill runs a targeted literature pass once the local discovery/prove process has localized a set of missing lemmas or barrier classes.

It is not a generic bibliography tool. It should only import decisive references that materially change how a blocked route is interpreted.

## When To Use It

Use it when:

1. the queue has stalled on named missing lemmas or repair lemmas;
2. a route may already be partly covered by prior art;
3. the next step is to distinguish a genuinely missing theorem from a theorem that already exists in the literature;
4. `InformalMathLib/<kb-ref>` is too thin to support novelty or barrier judgments.

## Workflow

1. Start from the blocked proof queue, proof-cycle summary, and current InformalMathLib.
2. Record the local-search failure that justifies browsing.
3. Identify the smallest set of missing lemmas or barrier classes that actually matter.
4. If the blocked frontier suggests a missing foundation rather than a missing exact lemma, search for a mathematical framework with the same structural role before broadening to generic literature.
5. Search only for decisive theorem, definition, or axiom level references.
6. Import those references into InformalMathLib as external-reference entries.
7. Emit a report explaining:
   which blocked classes were covered,
   what exact statements were imported,
   what changed in the proof state,
   and what still remains genuinely open.

## Guardrails

- Do not import decorative citations.
- Prefer paper-level primary sources or official open-access versions.
- State what changed because of each imported reference.
- Treat framework inspiration as admissible only when it sharpens the missing operation, preserved invariant, or target activation theorem.
- If a reference only grounds an already known target theorem, say so explicitly.
- If no exact prior art is found for a missing lemma, keep that lemma open rather than forcing a weak analogy into InformalMathLib.

## Deterministic Path

Use `scripts/generate_prior_art_pass_report.py`.

Example:

```text
python skills/discovery/kb-prior-art-pass/scripts/generate_prior_art_pass_report.py --artifacts-dir artifacts/p-vs-np --input-json artifacts/p-vs-np/prior-art-pass-input.json
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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_prior_art_pass_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
