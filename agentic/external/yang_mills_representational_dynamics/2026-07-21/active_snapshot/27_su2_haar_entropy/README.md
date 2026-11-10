# Stage 27: Exact SU(2) Haar Entropy

This stage proves and implements the exact Haar mass of geodesic balls and
shells in `SU(2)=S^3`, together with certified cubic small-ball entropy
brackets. It quantifies the denominator cost in the conditional
partition-ratio attack.

Run:

```bash
python3 -m unittest -v test_su2_haar_entropy.py
python3 su2_haar_entropy.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_haar_entropy_theorem.tex
```

The claim level is `C2`: exact finite geometry. No physical Yang--Mills
partition-ratio, basin-entry, continuum, or mass-gap theorem is claimed.
