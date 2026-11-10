# Stage 21: Curvature-Local Typical Sets and Atlas

The Stage 17 loss came from treating a local nonlinear constraint as one ball
in `408` dimensions.  This stage proves a dependency-safe local alternative.
On the Stage 8 Coulomb Gaussian, the four-link plaquette-input radius required
to make the union complement smaller than the degree-18 threshold is
approximately `0.00602316`, not `0.02463088`.

The stage also gives an exact two-center exponential atlas for all of `SU(2)`.
Every group element lies within radius `pi/2` of `+I` or `-I`; chart
multiplicity is at most two and the Haar-Jacobian ratio is at most
`(pi/2)^2`.  Probability charging of the nonprincipal channel remains open.

```bash
python3 -m unittest -v test_curvature_typical_set_atlas.py
python3 curvature_typical_set_atlas.py --output json
```

