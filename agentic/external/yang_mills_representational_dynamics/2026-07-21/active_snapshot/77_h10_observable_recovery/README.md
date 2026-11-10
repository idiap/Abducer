# Stage 77 — H10 exact finite observable recovery

This directory develops H10 as an exact C2 theorem on a clearly labeled
finite Z2 gauge toy model.  It constructs the orbit quotient and a canonical
reconstruction, proves exact recovery of a separating invariant observable
algebra, certifies a sharp two-step composition bound, and keeps erasure,
recovery, and probe completeness logically separate.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_observable_recovery.py
python3 observable_recovery.py --write
python3 -m json.tool observable_recovery_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h10_observable_recovery.json >/dev/null
```

The verified run contains 23 tests and 262,144 exact composition checks.
Python 3.11 or newer is sufficient; there are no third-party dependencies.

## Files

- `observable_recovery.py` — exact gauge action, quotient, reconstruction,
  invariant observable algebra, errors, composition theorem, and
  counterexamples.
- `test_observable_recovery.py` — typed-input, exhaustive, hostile, and claim
  guardrail tests.
- `observable_recovery_results.json` — canonical machine-readable output.
- `theorem_dependencies_h10_observable_recovery.json` — proof and physical
  dependency graph.
- `RESULT_LEDGER.md` — theorem statement, proof, calibrated examples,
  countermodels, and claim audit.
- `NEXT_STEP_TODOS.md` — finite SU(2), class, iteration, and continuum
  handoffs.

## Strongest conclusion

On the declared two-vertex, three-edge Z2 graph, the map

\[
B(e_0,e_1,e_2)=(e_0e_1,e_1e_2)
\]

is the exact gauge-orbit quotient and admits the section
\(R(y_1,y_2)=(1,y_1,y_1y_2)\).  The four Wilson characters form the complete
rational invariant algebra and are exactly recovered.  For every declared
observable and quotient maps \(f,g\),

\[
e_O(g\circ f)\le e_O(f)+e_O(g),
\]

with a finite example attaining equality.

## First open physical implication

Replace the toy graph by one normalized nonlinear finite SU(2) block with an
intrinsic quotient-valued retained state, then prove boundary-history-uniform
recovery estimates for a separating indexed Wilson/spin-network class.

