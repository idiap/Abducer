---
name: synthesize-portfolio
description: Retain the Pareto frontier, validation disagreements, uncertainty, and next discriminating actions. Use when a theory-discovery workflow needs this bounded portfolio-controller operation.
---

# Synthesize Portfolio

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `candidates`, `evaluations`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Compute the eligible Pareto frontier without scalar collapse.
2. Join supportive and adversarial validations by candidate while retaining disagreement and uncertainty.
3. Recommend promotion review, another discriminating test, suspension, or rejection; never hide failures.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill synthesize-portfolio --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `portfolio-controller`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.

## Human gate

Pause for explicit human review when promotion as substantive theory.

## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
