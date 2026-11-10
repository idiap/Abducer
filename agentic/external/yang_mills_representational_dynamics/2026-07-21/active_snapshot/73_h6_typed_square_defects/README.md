# Stage 73: H6 typed square defects

This stage mechanizes the finite and abstract core of H6 using exact rational
arithmetic. It closes the open B/C tasks from Stage 63 without assuming a
physical Yang--Mills realization.

## Contents

- `h6_typed_square_defects.py`: typed exact maps, tower composition,
  telescoping/recovery certificates, balanced-star certificate, and four
  counterexamples.
- `test_h6_typed_square_defects.py`: positive and hostile regression suite.
- `h6_typed_square_defects_results.json`: canonical exact result and defect
  ledgers.
- `theorem_dependencies_h6_typed.json`: claim dependency graph and downgrade
  boundary.
- `RESULT_LEDGER.md`: theorem, certificate, counterexample, and frontier
  summary.
- `NEXT_STEP_TODOS.md`: completed finite core and open physical handoff.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_h6_typed_square_defects.py
python3 h6_typed_square_defects.py --write
python3 -m json.tool h6_typed_square_defects_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h6_typed.json >/dev/null
```

## Claim boundary

The exact finite algebra is C2. No nonlinear `SU(2)` blocking map, positivity,
reflection positivity, cutoff-uniform limit, OS reconstruction, or Yang--Mills
mass gap is claimed.

The balanced-star result is exact for the displayed rational matrix. Stage 73
hashes that fixture but does not independently derive or hash-link it to Stage
70 geometry; geometric provenance remains open.
