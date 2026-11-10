# Stage 29: Coherence--Charge Trade-off

This stage proves the overlap-correct multi-link collar charge, incorporates
connected-witness entropy, and tests whether one coherence radius can control
both coherent and incoherent channels. The current certified regions are
disjoint even at ideal overlap one.

Run:

```bash
python3 -m unittest -v test_coherence_charge_tradeoff.py
python3 coherence_charge_tradeoff.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error coherence_charge_tradeoff_theorem.tex
```

This is a `C2` theorem about the current mechanism. It is not a physical
Yang--Mills basin-entry or mass-gap theorem.
