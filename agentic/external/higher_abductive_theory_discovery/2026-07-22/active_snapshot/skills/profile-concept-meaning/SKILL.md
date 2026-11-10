---
name: profile-concept-meaning
description: Reconstruct all nine dimensions of a concept's role in its native theory. Use when a theory-discovery workflow needs this bounded meaning-profiler operation.
---

# Profile Concept Meaning

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `concept_id`, `theory_id`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Reconstruct referential, inferential, identity, modal, operational, scope, explanatory, pragmatic, and protected-distinction components.
2. Ground each component in native sources where possible.
3. Mark missing components unknown and assign component-level uncertainty.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill profile-concept-meaning --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `meaning-profiler`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.


## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
