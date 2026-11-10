# Stage 70: H3 exact multi-star Gate B

This directory upgrades the Stage 52/60 floating multi-star signal to exact
rational certificates on the Paper 05 open side-two four-cube.

The result is stronger than the original probe:

- the adjacent pair is exactly coercive and has a fully rational spectrum;
- the central four has exactly four zero-spill modes and an exact
  quartic-cubed algebraic positive spectrum;
- all eight interior links have exactly seven zero-spill modes and a fully
  rational nonzero spectrum;
- center-before-orient is exactly falsified by its spurious one-star zero
  mode.

This is a C2 finite linearized theorem only. A growing-polymer boundary law,
coverage of bad-event directions, nonlinear `SU(2)` repair, and normalized
measure gain remain open.

## Reproduce

```bash
python3 exact_multistar.py --write
python3 exact_multistar.py --verify
python3 -m unittest -v test_exact_multistar.py
python3 -m json.tool exact_multistar_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h3_gate_b.json >/dev/null
```

The canonical data are in `exact_multistar_results.json`. Read
`RESULT_LEDGER.md` for the theorem statement and `NEXT_STEP_TODOS.md` for the
growing-family and physical handoff.

## Dependencies

- Paper 05 exact linear-algebra backend and orientation correction;
- Stage 43 centered-star formulation;
- Stage 44/45 one-star obstruction and repair-budget frontier;
- Stage 52 hypothesis probe;
- Stage 60 H3 stream report.

No root package documents or checksums are modified by this stream agent.
