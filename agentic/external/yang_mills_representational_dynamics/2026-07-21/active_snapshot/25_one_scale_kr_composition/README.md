# Stage 25: One-Scale K+R Composition

For positive bad subkernels `K` and `R`, normalized comparison
`K <= exp(ell) K0`, and `K0 V <= kV`, `RV <= rV`, this stage proves

```text
(K+R)V <= (exp(ell) k + r)V.
```

The local radius `0.00614955590043` gives half of the Stage 19 target budget
to the comparison-corrected reference channel and half to the residual
charged channel.  This lies inside the certified nonlinear window.  The
physical nonlinear `SU(2)` realization of `K+R` is open.

```bash
python3 -m unittest -v test_one_scale_kr_composition.py
python3 one_scale_kr_composition.py --output json
```
