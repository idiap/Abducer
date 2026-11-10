# Paper 03 — proof-bearing representation change

This directory is the complete, blinded submission candidate for:

> *When Does a Physical Property Survive Representation Change? Uniform
> Recovery, Spectral Rigidity, and the Yang--Mills Chain*

The paper develops a typed, property-relative calculus for exact preservation,
approximation, forgetting, recovery, and uniformity across representation
changes. Its central mathematical result is a uniform recovery-to-spectrum
theorem: convergence of positive semigroup quadratic forms on a dense centered
core, together with one index-independent exponential rate, excludes target
spectrum below that rate. Three exact countermodels isolate the necessity of
completeness, uniformity, and limit-order control.

The Yang--Mills application is methodological and conditional. The paper does
not construct four-dimensional continuum Yang--Mills theory, establish the OS
axioms, or prove a mass gap.

## Contents

- `main.tex`, `sections/`, `appendices/`, and `references.bib`: manuscript
  source;
- `build/main.pdf`: final 27-page blinded PDF;
- `artifacts/`: theorem, proof, literature, novelty, scope, and submission
  ledgers;
- `supplement/`: exact standard-library certificate code and 13 tests;
- `build/`: strict lint report, build report, log, extracted text, and visual
  previews.

## Reproduce

```bash
python3 supplement/representation_certificate.py \
  --output supplement/representation_certificate.json
python3 -m unittest -v supplement/test_representation_certificate.py
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -outdir=build_direct main.tex
```

The final PDF has no unresolved references or citations and no overfull boxes.
See `artifacts/verification_log.md` for checksums and `artifacts/frontier_audit.md`
for the strongest defensible claim.
