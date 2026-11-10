# Stage 22: Sharp Nonlinear Overlap

The previous nonlinear majorant used the global Banach-log second derivative
near value eight.  The exact plaquette-log Hessian at the identity has norm

```text
1+sqrt(2) = 2.41421356237...
```

Transporting this value with the already-certified third derivative produces
a rigorous sharper finite-radius certificate.  At the Stage 21 typical radius
`0.0060231578`, the total Hessian remainder is approximately `0.47467`, the
generated-base margin is approximately `0.68881`, and centered fiber transport
is approximately `0.06197`.

This proves a finite local overlap window.  It does not yet compare normalized
nonlinear and Gaussian conditional measures, charge the atlas complement, or
iterate an RG map.

```bash
python3 -m unittest -v test_sharp_nonlinear_overlap.py
python3 sharp_nonlinear_overlap.py --output json
```
