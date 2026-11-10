---
name: kb-macro-proof-paper-writer
description: Write the current macro-proof state as a mathematical paper-style narrative grounded in the main conjecture, and render it as Markdown, LaTeX, and PDF. Use when the user asks for a conjecture-centered current-state note, a macro-proof paper for a problem such as P vs NP, or a publication-style synthesis of the leading route, supporting routes, and proof frontier.
---

# KB Macro-Proof Paper Writer

## Conceptual Role

This skill converts the current artifact frontier into a paper-style macro-proof note. The note is not a claim of proof. It is a conjecture-centered state report that explains the strongest current route, how it bears on the main conjecture, what supporting routes exist, and what remains to be proved.

## Inputs

Run it after the following exist:

1. `expert-hypothesis-paper.json`
2. `proof-sketches.json`
3. `hypothesis-evaluation.json`
4. `proof-queue.json`
5. the problem KB itself

## Outputs

The deterministic generator emits:

1. `macro-proof-state.json`
2. `macro-proof-state.md`
3. `macro-proof-state.tex`
4. `macro-proof-state.pdf`
5. `macro-strategy-report.json`
6. `macro-strategy-report.md`
7. `macro-strategy-report.tex`
8. `macro-strategy-report.pdf`

## Workflow

1. Ground the leading route in the main conjecture.
2. State the logical implication chain from the current strongest payoff to the conjecture.
3. Present the leading bridge program in theorem-pair form.
4. Add the strongest supporting routes.
5. Add the current prove frontier from the queue.
6. End with an honest status assessment.
7. When the user asks what is still missing for completion, generate the macro-strategy report that isolates the unresolved proof package.

Read [references/script-usage.md](references/script-usage.md) for deterministic execution.
Read [references/prompt-template.md](references/prompt-template.md) for paper-style narrative guidance.

## Guardrails

- Do not blur conditional route success with an actual proof of the conjecture.
- Keep the paper mathematically grounded: main conjecture, theorem pair, carrier, invariant, route lemma, obligations, and failure logic.
- Make the stronger-than-target consequence explicit when relevant.
- Treat queue items as frontier tasks, not as solved lemmas.

## Deterministic Path

Use `scripts/generate_macro_proof_state_report.py` for the conjecture-centered state note.
Use `scripts/generate_macro_strategy_report.py` for the proof-completion strategy note.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Reporting must not launder conjectural, blocked, or low-relevance routes into conclusions.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: report section, handoff claim, expert summary, proof narrative, table, and cited artifact.
- Preserved invariants: claim-to-evidence mapping, status labels, target commitments, source limits, and unresolved obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `generate_macro_proof_state_report.py, generate_macro_strategy_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: claims with evidence paths or unknowns, epistemic status, target relevance, unresolved debt, demotion triggers, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote or annotate claims when evidence is missing, status is conjectural, disconfirmation is unresolved, or report prose overstates proof progress.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
