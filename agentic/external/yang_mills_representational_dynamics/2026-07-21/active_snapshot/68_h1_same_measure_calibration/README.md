# Stage 68: H1 same-measure calibration

This directory develops the next bounded H1 target.  It places the temporal
transfer, Gibbs edge weight, Perron vacuum, Doob dynamics, and masked bad
subkernel inside one finite reflection-positive two-state model.

The algebraically exact positive result is

\[
\frac{(QV)_i}{V_i}
=\frac{1}{\lambda_0}\sum_jM_{ij}T_{ij},
\qquad
V_i=\frac{\max\psi}{\psi_i}.
\]

The decisive negative result is the same-measure family

\[
T_\delta=\begin{pmatrix}1&\delta\\\delta&1\end{pmatrix},
\qquad
q(\delta)=\frac{\delta}{1+\delta}\to0,
\qquad
m_T(\delta)=-\log\frac{1-\delta}{1+\delta}\to0.
\]

Thus small weighted probability of one declared bad transition does not by
itself force a uniform lower bound on the full temporal spectrum.  The missing
bridge is a spectral observability/coercivity theorem ensuring that the
chosen defect channel sees every nonvacuum slow mode.

## Files

- `h1_same_measure.py` -- standard-library executable theorem and
  countermodel.
- `test_h1_same_measure.py` -- 18 hostile and positive tests.
- `h1_same_measure_results.json` -- canonical numerical certificate.
- `theorem_dependencies_h1_next.json` -- dependency and status graph.
- `RESULT_LEDGER.md` -- theorem, countermodel, and claim audit.
- `NEXT_STEP_TODOS.md` -- completed work and the next spectral-observability
  target.

## Reproduce

```bash
python3 h1_same_measure.py --write h1_same_measure_results.json
python3 -m unittest -v test_h1_same_measure.py
python3 -m json.tool h1_same_measure_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h1_next.json >/dev/null
```

## Scope

The classification is **C2: finite algebraic theorem with a floating-point,
tolerance-certified realization and a finite-family countermodel**.  This
stage does not construct the physical nonlinear
(SU(2)) kernel, establish uniformity in regulator limits, verify continuum
OS axioms, or prove a Yang--Mills mass gap.
