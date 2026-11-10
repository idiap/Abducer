# Stage 18: Adaptive Stochastic Domination

This stage replaces the open-ended “activity conversion” phrase by an exact
probabilistic theorem.  If every positive adaptive history has next-site bad
probability at most `q`, a shared-uniform sequential coupling places the bad
field below independent Bernoulli(`q`).  Connected-cluster bounds then follow
without identifying Mayer/Ursell activities.

At the Stage 14 weight `q=0.0024302775`, the degree-18 branching ratio remains
`0.8702225`.  The abstract conversion gate therefore closes.  The full
nonlinear `SU(2)` adaptive-history estimate is not proved.

The included two-site counterexample shows why this strengthening is
necessary: all intersection moments may obey `q^|S|` while stochastic
domination fails.

```bash
python3 -m unittest -v test_adaptive_stochastic_domination.py
python3 adaptive_stochastic_domination.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error adaptive_stochastic_domination_theorem.tex
```

Claim level: `C2` exact finite domination theorem with an open `SU(2)` premise.
