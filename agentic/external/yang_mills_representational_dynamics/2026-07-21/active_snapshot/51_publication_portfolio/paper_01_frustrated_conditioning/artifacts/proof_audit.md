# Proof audit

Audit date: 21 July 2026. Verdict: pass for the stated finite-lattice theorems.

## Quantifiers

- Fixed before the limit: dimension `d>=2`, block `B_d`, compact connected group `G`, bi-invariant metric, nonidentity central element `z`, target plaquette, and radius `0<rho<(m-1)dist(1,z)/m`.
- Sole limit: heat time `t downarrow 0`.
- Worst-boundary conclusion: supremum over all other microscopic link assignments.
- Stability conclusion: supremum over one explicitly constructed open boundary neighborhood.
- No volume, lattice-spacing, continuum, or Hamiltonian limit is implicit.

## Critical checks

| Check | Result |
|---|---|
| Incident degree and private opposite links | Symbolic cubical proof; exact matrix verifier agrees in `d=2,...,6`. |
| Orientation of conditional density | Both signs derived in Appendix A using inversion symmetry and cyclic conjugacy. |
| Heat-kernel normalization | Generator fixed as `1/2 Delta`; rate scale is `2t`. |
| Cut locus | Uniform logarithmic Varadhan theorem used; no prefactor or unique geodesic assumed. |
| Minimizer uniqueness | Corrected: only the distance pair is unique; the full set is described. |
| Open-set lower bound | Open and closed good-event infima are computed and shown equal. |
| Haar zero in SU(2) radial coordinates | Subexponential; the main proof is group-level and avoids radial endpoint issues. |
| Positive-measure stability | Proved by a retained compact energy gap plus uniform parameter Laplace bounds. |
| Dobrushin inference | Uses `m` distinct one-link changes; failure is only of the row criterion, not uniqueness. |
| Numerical dependence | None. All numerical diagnostics are dispensable. |

## Imported results

1. Heat-kernel positivity, centrality, inversion symmetry, and smoothness on a compact connected Lie group.
2. Varadhan's small-time logarithmic heat-kernel asymptotic, uniformly on compact point pairs.
3. Existence of minimizing geodesics on a compact Riemannian manifold.
4. Full support of normalized Haar measure.

Each imported result is used at its natural normalization. No imported theorem supplies the lattice realization or the conditional exponent.

## Residual referee risks

- A referee may request a more precise theorem/page citation for the uniform version of Varadhan's asymptotic. This is a bibliographic strengthening, not a missing proof mechanism.
- Some audiences define Dobrushin coefficients with an extra factor of `1/2` in an `L^1` norm. The manuscript defines total variation explicitly, so the limit one and row conclusion are convention-stable.
- A venue may prefer the compact-group extension as the main theorem and SU(2) as a corollary; the current organization already follows that ordering.
