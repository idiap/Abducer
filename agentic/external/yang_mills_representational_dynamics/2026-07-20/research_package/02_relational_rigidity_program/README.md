# Relational-rigidity programme for Yang--Mills

This package implements a representation-aware research programme for the
four-dimensional Yang--Mills existence and mass-gap problem.  It is deliberately
not presented as a solution of the Clay problem.

## Contents

- `ym_relational_rigidity_program.tex`: self-contained mathematical dossier.
- `ym_relational_rigidity_program.pdf`: compiled dossier.
- `proof_status_ledger.md`: theorem, assumption, and frontier ledger.
- `theorem_dependencies.json`: machine-readable dependency graph.
- `finite_spectral_core.py`: exact-arithmetic finite spectral and morphism core.
- `test_finite_spectral_core.py`: positive and adversarial unit tests.

## Reproduce

```bash
python3 -m unittest -v test_finite_spectral_core.py
latexmk -pdf -interaction=nonstopmode -halt-on-error ym_relational_rigidity_program.tex
```

## Epistemic boundary

The package proves finite spectral lemmas, representation-error composition,
an abstract noncircular basin-to-clustering theorem, and conditional
continuum/OS transfer theorems.  It does **not** prove that four-dimensional
pure Yang--Mills enters the proposed rigidity basin, nor does it construct the
required continuum theory.  Those are recorded as open frontier obligations.
