# Exact SU(2) heat-kernel local initializer

Stage 07 initializes the curvature-action part of the one-step norm.  It fixes
the heat-kernel convention on `SU(2) = S^3`, uses both the character and
Poisson-image representations, and produces explicit local derivative budgets.

For `0 < t <= 0.2` and class angle `theta <= 1`, the default certificate gives
approximately

```text
t ||Hess(s_t - theta^2/(2t))|| <= 0.0824566
t ||D^3(s_t - theta^2/(2t))|| <= 0.149094
```

It also encloses the gauge-invariant one-plaquette probability
`P_t(theta >= rho)` by integrating the character expansion and bounding the
omitted series.

## Files

- `su2_heat_kernel_initializer_theorem.{tex,pdf}`: theorem dossier.
- `su2_heat_kernel_initializer.py`: analytic bounds and calculators.
- `test_su2_heat_kernel_initializer.py`: representation and hostile tests.
- `su2_heat_kernel_calibration.json`: reproducible numerical output.
- `research_plan_todos.md`: completed target ledger.
- `su2_heat_kernel_frontier_ledger.md`: claim audit and first missing bridge.
- `theorem_dependencies_heat_kernel.json`: dependency graph.

## Reproduce

```bash
python3 -m unittest -v test_su2_heat_kernel_initializer.py
python3 su2_heat_kernel_initializer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_heat_kernel_initializer_theorem.tex
```

Requires Python 3.10 or later and NumPy 2.x.
