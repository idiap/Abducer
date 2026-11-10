---
name: propose-theory-morphism
description: Stage a symbol and scope interpretation with explicit satisfaction obligations. Use when a theory-discovery workflow needs this bounded atlas-cartographer operation.
---

# Propose Theory Morphism

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `source_fragment`, `target_fragment`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Declare source and target fragments and the mapping domain.
2. Map every declared source symbol and every scope restriction.
3. Emit typing, satisfaction, and scope-preservation obligations; keep the map staged.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill propose-theory-morphism --input INPUT.json --pretty
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
