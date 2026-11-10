---
name: scope-research-context
description: Freeze the question, scope, goals, protections, success, stop criteria, and budgets. Use when a theory-discovery workflow needs this bounded portfolio-controller operation.
---

# Scope Research Context

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `question`, `goals`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Separate the research question from preferred answers.
2. Make scope, regime, protected commitments, success criteria, stop criteria, and budgets explicit.
3. Stage the context and request human review for later goal or commitment changes.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill scope-research-context --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `portfolio-controller`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.

## Human gate

Pause for explicit human review when goal or protected-commitment change.

## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
