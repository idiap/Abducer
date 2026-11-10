# Nonlinear `SU(2)` geometry on the `2^4` block

Stage 08 closes the next finite-dimensional representation bridge.  It
combines an exact unit-quaternion realization of `SU(2)`, explicit
Banach-logarithm derivative bounds, the side-two four-cube incidence complex,
and the Stage 07 heat-kernel certificate.

For the calibrated ultraviolet chart

```text
t_max = 0.01
local four-link radius = 0.003
plaquette curvature radius = 0.006
fiber tube radius = 0.001
```

the implementation initializes all five Stage 06 good-chart norm components,
certifies centered-fiber contraction, and leaves a positive generated-base
reference margin.  A separate local gauge-slice certificate takes a link field
of norm at most `0.0002` into this chart using a mean-zero gauge parameter ball
of radius `0.0006`.

The same computation shows why the result is not yet a full-measure theorem:
at `t=0.01`, the one-plaquette probability of lying outside curvature radius
`0.006` is greater than `0.9999`.  Sharper geometry and a dependent polymer
argument are therefore required.

## Files

- `su2_nonlinear_block_geometry_theorem.{tex,pdf}`: theorem dossier.
- `su2_nonlinear_block_geometry.py`: quaternion, incidence, slice, and norm
  certificates.
- `test_su2_nonlinear_block_geometry.py`: positive and hostile tests.
- `su2_nonlinear_block_calibration.json`: reproducible default certificate.
- `research_plan_todos.md`: completed research plan.
- `su2_nonlinear_block_frontier_ledger.md`: claim and blocker audit.
- `restricted_model_audit.md`: parameter, calibration, representation, and
  limit audit.
- `theorem_dependencies_nonlinear_block.json`: machine-readable dependency
  graph.

## Reproduce

```bash
python3 -m unittest -v test_su2_nonlinear_block_geometry.py
python3 su2_nonlinear_block_geometry.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  su2_nonlinear_block_geometry_theorem.tex
```

The code requires Python 3.10 or later, NumPy, and the adjacent Stage 07 module.
