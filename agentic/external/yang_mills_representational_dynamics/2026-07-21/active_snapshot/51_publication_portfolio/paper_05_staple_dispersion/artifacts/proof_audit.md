# Analytic proof audit

## Checks passed

- The gauge transformation of a staple is left/right, not conjugation; the
  bitorsor language and bi-invariant distance handle this correctly.
- The Fréchet minimizer exists by compactness; stationarity is invoked only in
  the chart avoiding the cut locus.
- The lower spherical comparison uses the logarithm along the minimizing
  geodesic inside a strongly convex ball.  It does not reverse the inequality
  between distance and an arbitrary path length.
- The exact Gaussian law includes color multiplicity three and has moment
  domain `s < 35/(33t)`.
- The mean is `3t tr(K)=1369t/210`.
- The spill form uses a generalized metric because the rational centered basis
  is not orthonormal.
- Full KKT substitution makes the minimum exact even though the Hessian and
  KKT matrix are singular.
- The central link has no effect on either centered-star or external maps.
- The repair discussion does not infer that positive spill forbids total
  action reduction.

## Remaining reviewer-sensitive points

- The Fréchet comparison assumes a selected stationary minimizer and a radius
  bound about that minimizer; it does not prove basin entry into that chart.
- The geodesic-quadratic plaquette action is a diagnostic/small-field model,
  not the Wilson action itself.
- Standalone novelty of the exact block spectrum requires expert literature
  confirmation.
