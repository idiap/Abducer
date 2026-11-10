---
name: audit-reasoning-run
description: Audit provenance, authority separation, budgets, scope drift, and replay completeness. Use when a theory-discovery workflow needs this bounded integrity-auditor operation.
---

# Audit Reasoning Run

Perform one bounded epistemic operation and return the common `SkillResult` envelope. Treat generated material as staged and conjectural until an independent validator accepts it.

## Inputs

Require `trace`. Validate the complete input against `input.schema.json`. Preserve source locators, scope, regime, uncertainty, and parent artifact identifiers.

## Procedure

1. Verify source and replay provenance for every event.
2. Check that generators did not validate their own candidates.
3. Check budget compliance, scope drift, terminal conditions, and deterministic replay; emit remediations for every failure.

## Runtime

When the `tdr` package is installed, run:

```bash
python -m tdr.api.cli run-skill audit-reasoning-run --input INPUT.json --pretty
```

The executable wrapper is `scripts/run_skill.py`. If the runtime is unavailable, follow the procedure directly and still emit the exact envelope in `output.schema.json`.

## Boundaries

- Act only as `integrity-auditor`; do not approve your own generative output.
- Do not infer truth, novelty, or identity from relevance, graph structure, embeddings, or fluent prose.
- Keep incompatible interpretations separate until a validated equivalence or synthesis exists.
- Return `blocked` with missing information when preconditions fail; do not silently guess.
- Stop after one bounded operation or when the policy budget is exhausted.


## Output

Return `status`, `artifacts`, `claims`, `uncertainties`, `next`, and `provenance`. Label each claim as sourced, conjectural, interpretive, validated, or falsified as applicable.
