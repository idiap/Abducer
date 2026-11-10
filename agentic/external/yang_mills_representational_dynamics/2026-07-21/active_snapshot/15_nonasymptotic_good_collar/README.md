# Stage 15: Nonasymptotic Good-Collar Conditionals

This stage upgrades the Stage 11 small-time rate theorem to an explicit
finite-time `SU(2)` bound.  It retains the normalized Haar volume of the
denominator ball and the Poisson-image heat-kernel remainder.

At the frozen witness `t=3e-6`, the rigorous prefactor bound is trivial.  The
same theorem crosses the Stage 14 critical bad weight at approximately
`t=8.994203e-7`.  This is a theorem under a supplied coherent collar, not a
proof that the interacting measure supplies such collars.

```bash
python3 -m unittest -v test_nonasymptotic_good_collar.py
python3 nonasymptotic_good_collar.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error nonasymptotic_good_collar_theorem.tex
```

Claim level: `C2` finite-time one-link theorem under a coherent-collar
hypothesis.
