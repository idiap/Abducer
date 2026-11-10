# Stage 28: Coherent Partition Optimizer

This stage certifies the unique Haar-denominator optimizer in the finite-time
coherent-staple conditional bound and re-optimizes the one-scale `K+R` radius.
It closes the coherent channel conditionally inside the existing nonlinear
window.

Run:

```bash
python3 -m unittest -v test_coherent_partition_optimizer.py
python3 coherent_partition_optimizer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error coherent_partition_optimizer_theorem.tex
```

The collar-occurrence law and complete nonlinear `SU(2)` partition ratio remain
open, so the claim level stays `C2`.
