# Paper 04: global arbitrary-order SU(2) heat-kernel enclosures

This directory is a self-contained manuscript and reproducibility supplement.
Its standalone theorem gives computable finite-order derivative bounds for the
SU(2) heat-kernel action on a complete three-chart cover, together with the
Morse--Bott antipodal prefactor and normalized tails. It makes no continuum or
mass-gap claim.

Core outputs:

- `main.tex` and `build/main.pdf`
- `conceptual_explainer.tex` and
  `build/conceptual_explainer/conceptual_explainer.pdf`
- `supplement/exact_enclosures.py`
- `supplement/heat_kernel_certificate.json`
- `supplement/verify_certificate.py`
- `supplement/test_heat_kernel_enclosures.py`
- `artifacts/` for proof, literature, novelty, verification, and scope audits

Reproduce with:

```bash
python3 supplement/exact_enclosures.py
python3 supplement/verify_certificate.py
python3 -m unittest supplement.test_heat_kernel_enclosures -v
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The portable release archive is stored beside this directory as
`paper_04_heat_kernel_enclosures_revised.zip` with a SHA-256 sidecar.
