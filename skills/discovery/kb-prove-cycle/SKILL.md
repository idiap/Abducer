---
name: kb-prove-cycle
description: "Run the prove cycle over the persistent proof queue: consume one queued claim, attempt an informal proof or disproof, apply systematic critique judges, use web search only under a parsimonious gate, and persist terminal positive or negative results into a problem-scoped InformalMathLib plus a summary report."
---

# KB Prove Cycle

## Conceptual Role

This skill turns one queued proof target into an auditable informal proof or disproof attempt.

## When To Use It

Use it when a user asks to:

1. consume the next proof target from the queue;
2. attempt an informal proof or negative result;
3. run systematic critique over each proof step;
4. persist proved/disproved results into a problem-scoped InformalMathLib.

## Workflow

1. Start from the persistent queue.
Consume exactly one queue item and scaffold a proof dossier with:
proof target stated as a self-contained conjecture,
route lemma under test,
local KB grounding,
local InformalMathLib hits,
web-search gate,
critique judges.

2. Work locally first.
Use the queue item, KB, existing artifacts, and InformalMathLib before considering web search.

3. Attempt an informal proof or disproof.
Write the argument step-by-step, keeping assumptions explicit and organizing the proof through an informal tactic trace inspired by proof-assistant moves such as `intro`, `have`, `suffices`, `obtain`, `apply`, contradiction, negation, impossibility framing, and obstruction probing.

4. Run critique judges.
Every terminal outcome must pass through the systematic judge set, including tactic-aware judges that inspect goal control, tactic-trace discipline, and explicit subgoal exposure.

5. Apply the web-search gate parsimoniously.
Browse only if the policy in [references/web-search-policy.md](references/web-search-policy.md) is triggered.

6. Finalize.
Persist positive or negative terminal results into `InformalMathLib/<kb-ref>/...`, update the queue state, and refresh the proof-cycle summary report.
Also import any externally cited theorem, definition, or axiom into the same problem-scoped InformalMathLib as a searchable external-reference entry.
If a proved or disproved intermediate result clears the major-subresult threshold, also emit a standalone LaTeX/PDF paper into `artifacts/<kb-ref>/produced_papers/`.

Read [references/prompt-template.md](references/prompt-template.md) for the proof-cycle prompt.
Read [references/critique-judges.md](references/critique-judges.md) for the mandatory critique structure.
Read [references/web-search-policy.md](references/web-search-policy.md) before any browsing.

## Guardrails

- Do not claim a proof when the result is only a plausible sketch.
- Do not browse unless the web-search gate is triggered.
- If prior art is found, classify the outcome as `prior_art_found` rather than novelty.
- Negative results are first-class outcomes if they are explicit, theorem-shaped, and informative.
- Contradiction and impossibility reasoning should be represented explicitly, not only as vague obstruction prose.
- Every proof step must be inspectable by a mathematical expert.

## Deterministic Path

Use `scripts/start_proof_cycle.py` to consume the next queue item and create the dossier.
Use `scripts/finalize_proof_cycle.py` after the attempt is filled in.
Use `scripts/generate_proof_cycle_summary.py` to refresh the summary independently if needed.

Examples:

```text
python skills/discovery/kb-prove-cycle/scripts/start_proof_cycle.py --kb kb/p-vs-np.kb.md --artifacts-dir artifacts/p-vs-np
python skills/discovery/kb-prove-cycle/scripts/finalize_proof_cycle.py --kb-ref p-vs-np --attempt-json artifacts/p-vs-np/proof-attempts/attempt.p-vs-np.001.json --outcome blocked
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

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `finalize_proof_cycle.py, generate_proof_cycle_summary.py, generate_proof_queue_report.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
