# Stage 75 — H8 certified retained-state refinement

This directory develops H8 as an exact finite C2 theorem. It replaces the
rounded Stage 52 probe by rational signature refinement, proves the coarsest
stable property, emits exact split witnesses, and exercises cross-stage and
hostile regressions.

The Stage 19 decimal is parsed as an exact rational fixture. Exactness applies
to that rational kernel identity, not to independent recovery of an
underlying real parameter.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_certified_refinement.py
python3 certified_refinement.py
python3 -m json.tool exact_refinement_results.json >/dev/null
```

The verified run contains 18 tests. Python 3.11 or newer is sufficient; the
module has no third-party dependencies.

## Files

- `certified_refinement.py` — exact refinement, witnesses, exhaustive checker,
  equivariance tests, regressions, and state-explosion diagnostics.
- `test_certified_refinement.py` — positive, boundary, malformed-input, and
  tampered-certificate tests.
- `exact_refinement_results.json` — canonical machine-readable output.
- `theorem_dependencies_h8_refinement.json` — theorem and physical-frontier
  dependency graph.
- `RESULT_LEDGER.md` — statement, proof, calibrated results, and claim audit.
- `NEXT_STEP_TODOS.md` — physical-table, interval, compression, weighted, and
  continuum handoffs.

## Strongest conclusion

For a declared finite sub-Markov kernel and seed partition, the algorithm
terminates at the unique coarsest stable refinement after at most \(n-b\)
strict rounds. This is exact and permutation-equivariant. It is not a
construction of the physical nonlinear SU(2) retained-boundary table.

## First open physical implication

Construct that normalized SU(2) table, with a gauge-invariant seed partition,
then prove that the stable state count, weighted defect ceiling, and root
moment remain uniform in cutoff and volume.
