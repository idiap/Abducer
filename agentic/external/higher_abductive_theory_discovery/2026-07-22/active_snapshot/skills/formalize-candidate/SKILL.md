---
name: formalize-candidate
description: Compile a candidate into formal skeletons and exact proof obligations. Use when a theory-discovery workflow needs this bounded formalizer-and-prover operation.
---

# Formalize Candidate

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `candidate`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Compile the candidate into declared formal objects and obligations.
2. Check local typing and syntax before invoking an optional formal adapter.
3. Return exact blockers or residual proof obligations; do not claim proof from generated skeletons.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill formalize-candidate --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `formalizer-and-prover`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.


## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
