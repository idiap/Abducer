# Stage 11: Coherent-Staple Good Collar

This stage proves the boundary-restricted counterpart to the Stage 10
obstruction.  If the six staples surrounding a selected link lie in a common
geodesic ball of radius `eta`, then every target plaquette has a uniform
small-time conditional rate gap at least

```text
rho^2 - 6 eta^2.
```

At `rho=0.0082` and `eta=0.001` the gap is positive.  The center-frustrated
Stage 10 boundary needs coherence radius `pi/2`, so it is excluded.

The theorem does not bound the probability that the collar is coherent.  That
is the charged-contour target of Stage 12.

## Reproduce

```bash
python3 -m unittest -v test_good_collar_coherence.py
python3 good_collar_coherence.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error good_collar_coherence_theorem.tex
```

Claim level: `C2`, uniform small-time theorem under an explicit good-collar
hypothesis.

