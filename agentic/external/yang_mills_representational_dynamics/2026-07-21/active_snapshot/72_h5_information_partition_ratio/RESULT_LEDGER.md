# H5 result ledger

| ID | Result | Status | Level | What it does not establish |
|---|---|---:|---:|---|
| H5-72-A | `inf_{nu(B)=1} D(nu||mu) = -log mu(B)`, uniquely minimized by `mu(.|B)` up to null sets | proved, finite | C1 | A lower bound for the physical bad event |
| H5-72-B | Deterministic coarse maps cannot increase KL divergence | mathematical theorem; numerically checked on finite fixtures | C1 | Defect independence or a positive quasi-factorization constant |
| H5-72-C | `mu(B)<=epsilon` iff `Z_B/Z_G<=epsilon/(1-epsilon)` for positive restricted normalizers | proved, finite | C1 | Uniform control of either physical restricted partition function |
| H5-72-D | Multiplicity can overwhelm action penalty; a collapsing good normalizer can make a vanishing bad numerator have probability tending to one | explicit counterexamples | C1 | A quantitative theorem for nonlinear lattice gauge measure |
| H5-72-E | `D(nu||tensor mu_j) >= sum_j D(nu_j||mu_j)` with residual equal to total correlation | proved, finite product model | C2 restricted | The same inequality for interacting or constrained measures |
| H5-72-F | Product all-bad event has exactly additive information cost and exponential probability | proved, finite product model | C2 restricted | A boundary-uniform polymer/defect estimate |
| H5-72-G | A full-support common-bit mixture has admissible `c_QF` ceiling approaching `1/n` | explicit interacting counterexample | C1 | Impossibility under additional mixing assumptions |
| H5-72-H | Uniform nonlinear Yang--Mills partition ratio or quasi-factorization | open | C2 target | — |

All executable KL and ratio values are binary floating-point evaluations.
Exactness refers to the displayed mathematical identities. For the common-bit
family, `full_support` records the mathematical fact
\(e^{-n^2}>0\); a separate flag records numerical underflow.

## Strongest finite conclusion

For a product reference measure,

```text
D(nu || tensor_j mu_j)
  = sum_j D(nu_j || mu_j) + D(nu || tensor_j nu_j),
```

so the defect quasi-factorization constant is exactly `c_QF=1`. For a
correlated full-support family, conditioning on one common all-bad atom pays a
global information cost once while each local observation repeats essentially
the same cost. At 20 blocks the resulting upper bound on `c_QF` is `0.05`.

## First open physical implication

Prove either a bad/good restricted partition-ratio inequality or a defect
quasi-factorization with strictly positive constants uniform in finite volume,
boundary data, cutoff, and positive-mass retained history for the actual
nonlinear constrained Yang--Mills conditional measure. Data processing by
itself cannot supply this theorem.
