# Stage 13: Dependent Gaussian Polymers

The linearized gauge quotient has curvature

```text
F ~ N(0, t P tensor I_3),
```

where `P` is the orthogonal projection onto exact plaquette curvatures.  This
retains shared-link and Bianchi dependence.  Since `P<=I`, a quadratic moment
gives an exponential simultaneous-defect estimate for every plaquette set.
Combining it with the exact degree-18 plaquette adjacency graph yields a rooted
connected bad-event bound without an independence assumption.  It is an
activity envelope, not yet a Mayer/Ursell expansion.

At the Stage 09 witness the bound is strictly subcritical.  This is exact for
the linearized Gaussian model; nonlinear `SU(2)` comparison remains open.

## Reproduce

```bash
python3 -m unittest -v test_dependent_gaussian_polymers.py
python3 dependent_gaussian_polymers.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error dependent_gaussian_polymers_theorem.tex
```

Claim level: `C2`, exact dependent Gaussian gauge theorem.
