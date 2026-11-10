---
name: run-philosophical-reflection
description: Run eight independent lenses and compile redescription, loss, counterworld, and obligation records. Use when a theory-discovery workflow needs this bounded philosophical-reflector operation.
---

# Run Philosophical Reflection

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `site`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Run hermeneutic, phenomenological-operational, constitutive, dialectical, genealogical, pragmatic, structural-realist, and modal-counterfactual lenses independently.
2. Compare convergence, contradiction, and complementarity.
3. Produce at least three redescriptions, including a primitive shift and a conservative option, plus losses, counterworlds, and formal/concrete obligations.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill run-philosophical-reflection --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `philosophical-reflector`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.

## Human gate

Pause for explicit human review when genuine ontological or value choice.

## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
