# Four-dimensional SU(2) quotient-fiber block

This package implements the next bounded target in the representation-aware
Yang--Mills programme: an explicit `2^4` cubical block at the tangent-field
level, tensored with `su(2)`.

It constructs the cubical cochain complex, removes infinitesimal gauge
directions, retains coarse boundary-face curvature data, identifies the
conditional fiber, and computes its Gaussian coercivity and transport data.

## Files

- `su2_quotient_fiber_theorem.tex` and `.pdf`: theorem dossier.
- `su2_block_linearized.py`: cubical complex and Gaussian fiber analysis.
- `test_su2_block_linearized.py`: positive and adversarial tests.
- `su2_block_calibration.json`: reproducible finite-block results.
- `research_plan_todos.md`: plan and completed todo ledger.
- `su2_frontier_ledger.md`: claim levels and open nonlinear/RG obligations.
- `theorem_dependencies_su2.json`: machine-readable dependency graph.

## Reproduce

```bash
python3 -m unittest -v test_su2_block_linearized.py
python3 su2_block_linearized.py --output json > su2_block_calibration.json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_quotient_fiber_theorem.tex
```

The exact unconditional result concerns the Gaussian tangent theory on one
finite four-dimensional block. The nonlinear small-field theorem is a
stability implication from explicit derivative bounds. Full-measure control,
iteration through a diverging number of RG scales, the nonperturbative
crossover, and continuum construction remain open.
