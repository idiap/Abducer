# Paper 05: staple dispersion and curvature spillover

This directory contains a self-contained 15-page mathematical-physics
manuscript and exact reproducibility supplement.  Its strongest result is the
strictly positive minimum external-curvature spectrum for lifting a centered
six-staple displacement on every interior link of the open side-two
four-dimensional block.

Core outputs:

- `main.tex` and `build/main.pdf`
- `supplement/exact_linear_algebra.py`
- `supplement/staple_dispersion_certificate.json`
- `supplement/test_exact_linear_algebra.py`
- `artifacts/` for literature, novelty, proof, orientation, scope, and visual
  audits

Reproduce with:

```bash
python3 supplement/exact_linear_algebra.py --verify
python3 -m unittest supplement.test_exact_linear_algebra -v
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The claim level is `C2`: finite-block exact linear algebra plus a local
nonlinear geometric theorem.  No interacting nonlinear measure, repeated RG,
continuum theory, or mass gap is proved.

The portable submission archive and its SHA-256 sidecar are stored beside this
directory.
