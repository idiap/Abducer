# One-step generated effective-action theorem

This stage closes the finite-dimensional algebraic step that was left open by
the explicit four-dimensional `SU(2)` quotient/fiber block.  It defines a
scaled local action norm and proves explicit recursion formulas under one exact
fiber marginalization.

The main output is

```text
mu          = lambda_fiber - eps_fiber
h           = eps_cross / mu
chi(r)      = r (tau_cross + tau_fiber h)
K_fiber(r)  = chi(r) / mu
eta_good    = eps_base + eps_cross^2 / mu
eta_defect  = zeta_hessian + zeta_gradient^2
eta_full    = eta_good + eta_defect
```

These are rigorous implications from the declared derivative and defect
bounds.  The stage does not prove that a full four-dimensional Yang--Mills RG
step satisfies those inputs.

## Files

- `one_step_effective_action_theorem.{tex,pdf}`: theorem dossier.
- `one_step_effective_action.py`: certificate calculator and Gaussian witness.
- `test_one_step_effective_action.py`: positive, boundary, and hostile tests.
- `one_step_calibration.json`: reproducible certificate examples.
- `research_plan_todos.md`: target and completed todos.
- `one_step_frontier_ledger.md`: claim audit and first missing implication.
- `theorem_dependencies_one_step.json`: machine-readable dependency graph.

## Reproduce

```bash
python3 -m unittest -v test_one_step_effective_action.py
python3 one_step_effective_action.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error one_step_effective_action_theorem.tex
```

Requires Python 3.10 or later and NumPy 2.x.
