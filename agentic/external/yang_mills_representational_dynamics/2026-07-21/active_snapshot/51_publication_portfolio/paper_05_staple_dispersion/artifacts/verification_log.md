# Verification log

Date: 21 July 2026.

## Exact certificate

`python3 supplement/exact_linear_algebra.py --write` rebuilt the canonical
certificate.  It verified eight rational projection systems, eight full
integer/rational KKT systems, and the corresponding exact characteristic
polynomials.

## Tests

`python3 -m unittest supplement.test_exact_linear_algebra -v`

- 5 tests run in 21.043 seconds;
- block counts and incidence properties: pass;
- oriented Gaussian spectrum: pass;
- polynomial determinant backend: pass;
- strictly positive spillover spectrum: pass;
- stored certificate equality: pass.

## LaTeX

`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`

- output: 15 pages, 408,204 bytes;
- citations and references: resolved;
- LaTeX warnings: zero;
- overfull/underfull boxes: zero;
- extracted text: 5,606 words.

Hashes are recorded in `build/build_report.json`.
