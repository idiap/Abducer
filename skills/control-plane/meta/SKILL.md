---
name: meta
description: Reflect on the nature of the current mathematical discovery process from a chosen perspective, explain why the original problem remains hard, interpret the present proof state and intermediate results, and identify what has genuinely shifted or persisted in understanding. Use when the user asks for meta-analysis, reflective interpretation of the discovery process, or how the current search changed the problem framing.
---

# Meta

## Conceptual Role

This is the meta-analytical reflection layer for the platform.
It does not ask only which route is best.
It asks what the current search has actually taught us about the problem, what remains structurally hard, and how the present bridge and proof artifacts changed the research perspective.

## When To Use It

Use it when the current artifact set already contains:

1. `epistemic-hardness.json`
2. `macro-proof-state.json`
3. `macro-strategy-report.json`
4. `proof-cycle-summary.json`
5. `end-to-end-proof-plausibility.json`

It is appropriate when the user asks:

1. why the original problem is hard and whether that changed;
2. how the discovery plus prove process altered the interpretation of the problem;
3. what the current intermediate results mean at a meta level;
4. how understanding shifted, persisted, or regressed;
5. for a reflective report in `.md`, `.tex`, `.pdf`, or `.json`.

## Workflow

1. Read the current hardness, macro-proof, macro-strategy, proof-cycle, proof-critic, promising-directions, and search-space-tree artifacts.
2. Choose a perspective from [references/perspectives.md](references/perspectives.md).
3. Interpret the current state through that perspective:
   original hardness,
   current proof-state reading,
   what shifted,
   what persisted,
   what intermediate results already changed expert understanding.
4. Classify each major change as:
   perspective shift,
   sharpening,
   persistence,
   unresolved defect,
   or regression.
5. Emit a meta reflection report with explicit references and a final meta-judgment.

Read [references/perspectives.md](references/perspectives.md) for the supported lenses.
Read [references/shift-taxonomy.md](references/shift-taxonomy.md) for the shift classes.
Read [references/prompt-template.md](references/prompt-template.md) for the prompt shape.

## Guardrails

- Do not confuse richer artifacts with actual mathematical progress.
- Distinguish clearly between:
  grounded change in understanding,
  improved organization,
  and proved new mathematics.
- Treat persistent hardness as a first-class outcome.
- Reflect on intermediate results in content terms, not only score or workflow terms.
- Keep the final judgment conservative when terminal proof evidence is absent.

## Deterministic Path

Use `scripts/generate_meta_reflection_report.py`.

For an external-expert slide narrative over the current `work` + `meta` state, use `scripts/generate_discovery_process_slides.py`.

Example:

```text
python skills/control-plane/meta/scripts/generate_meta_reflection_report.py --artifacts-dir artifacts/p-vs-np --perspective epistemic --interpretation balanced
```

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Workflow validity is not theorem validity; never promote a mathematical claim merely because a hook, report, or release gate passed.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: target packet, dependency graph node, workflow contract, hook decision, gate packet, and release artifact.
- Preserved invariants: target identity, declared dependencies, gate semantics, artifact provenance, and unresolved proof debt.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `archive_legacy_reports.py, generate_discovery_process_slides.py, generate_epistemic_process_map.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: decision, cited evidence paths or explicit unknowns, unresolved mathematical debt, rollback/quarantine condition, and next validator. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote or quarantine on uncited artifacts, missing target packet IDs, hidden hooks, stale gates, unsupported proof claims, or drift from essential target commitments.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
