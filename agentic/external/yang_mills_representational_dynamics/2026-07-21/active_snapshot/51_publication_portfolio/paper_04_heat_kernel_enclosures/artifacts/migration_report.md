# Migration from the earlier local calibration

The earlier floating calibration treated orders zero through three at
`t0=0.2`, `rho=1`. Paper 04 replaces it with a proof family and certifies
orders zero through eight.

- The old scaled Hessian remainder, approximately `0.08246`, is below the new
  rational majorant `t0*(G2+B2) < 0.091`.
- The old scaled third-tensor budget, approximately `0.1491`, is below the
  conservative radial-to-tensor majorant `4*t0*(G3+B3) < 0.232`.
- The earlier image correction is contained because each new `Q_m` is an
  analytic supremum with an omitted-image tail.
- The new constants are deliberately looser but theorem-critical and
  portable; the earlier floats remain useful sharpness diagnostics.
