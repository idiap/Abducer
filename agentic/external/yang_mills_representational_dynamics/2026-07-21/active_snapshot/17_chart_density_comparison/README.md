# Stage 17: Chart Density Comparison

This stage proves the normalized comparison theorem needed to transport a
Gaussian event estimate through a nonlinear chart.  The total logarithmic
loss is the sum of action-remainder oscillation and chart-coverage loss.

For the Stage 08 inner ball at `t=3e-6`, the action oscillation is only
`6.35e-6`, but the certified 408-dimensional Gaussian log mass is
`-803.25266`.  Even divided across 216 plaquettes, the resulting loss
`3.71876` exceeds the Stage 14 target `0.2`.  The inner-ball coverage bound is
deliberately conservative; the result identifies the missing atlas/coverage
theorem rather than proving the actual chart mass is small.

```bash
python3 -m unittest -v test_chart_density_comparison.py
python3 chart_density_comparison.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error chart_density_comparison_theorem.tex
```

Claim level: `C2` normalized density comparison and restricted finite-block
calibration.
