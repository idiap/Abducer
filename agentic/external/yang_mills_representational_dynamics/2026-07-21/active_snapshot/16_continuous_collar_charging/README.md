# Stage 16: Continuous Collar Charging

This stage proves an exact continuous nonabelian charge for incoherent staple
collars.  Relative staple distances equal relative incident-plaquette
distances for every selected-link value.  Consequently, failure of a common
`eta`-ball forces one incident curvature above `eta/2` and total incident
squared curvature above `eta^2/2`.

The result also proves a quantitative no-go for the simplest local repair.  At
the frozen witness, the largest exponent compatible with the Stage 11 collar
threshold is `0.9338889`, while Stage 14 requires about `6.67`--`7`.

```bash
python3 -m unittest -v test_continuous_collar_charging.py
python3 continuous_collar_charging.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error continuous_collar_charging_theorem.tex
```

Claim level: `C2` exact deterministic geometry and restricted Gaussian
compatibility theorem.
