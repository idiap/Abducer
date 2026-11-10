---
name: instantiate-concretely
description: Construct mathematical or physical return plans, models, observables, and error obligations. Use when a theory-discovery workflow needs this bounded concrete-instantiator operation.
---

# Instantiate Concretely

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `candidate`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Choose target mathematical models and, where applicable, physical systems or experiments.
2. Construct the abstract-to-concrete and return maps.
3. Supply equations or executable plans, approximation assumptions, error bounds, and discriminating outcomes.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill instantiate-concretely --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `concrete-instantiator`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.


## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
