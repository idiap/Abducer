---
name: map-theory-fragment
description: Extract source-addressable typed theory fragments while retaining regime metadata. Use when a theory-discovery workflow needs this bounded atlas-cartographer operation.
---

# Map Theory Fragment

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `sources`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Segment source-addressable definitions, types, symbols, axioms, claims, models, observables, and scopes.
2. Mark an unsourced proposal as conjectural; never present it as extracted fact.
3. Stage the fragment; do not merge it into an accepted atlas.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill map-theory-fragment --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `atlas-cartographer`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.


## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
