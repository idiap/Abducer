# Stage 23: Local-Cylinder Normalized Comparison

This stage replaces the inappropriate global `408`-dimensional inner ball by
the dependency-safe intersection of the local four-link cylinders certified
in Stage 21.  The normalized restriction theorem gives the logarithmic loss

```text
m kappa - log(1-delta).
```

At the frozen centered reference, the loss is `3.01676e-5` per support unit,
well below the declared `0.2` target.  Uniformity over all retained nonlinear
`SU(2)` boundary states remains open.

```bash
python3 -m unittest -v test_local_cylinder_comparison.py
python3 local_cylinder_comparison.py --output json
```
