# H7 atlas and reconstruction stream

## Scope and status

H7 is the representational claim that local nonlinear Yang--Mills control can be reconstructed without forcing every link into one principal logarithm chart. Its proved input is substantial but finite: the two exponential charts centered at `+I` and `-I`, each of radius `pi/2`, cover all of `SU(2)`; chart multiplicity is at most two; and the Haar-Jacobian ratio on either chart is at most `(pi/2)^2`. Relative tree gauge also gives an exact finite-graph quotient and Haar disintegration into retained boundary state and conditional interior fiber. At the dependency-aware four-link radius `r_* = 0.006023157807602598`, the sharpened plaquette-log Hessian estimate proves a finite nonlinear overlap window. These are C2 analytic or finite representation theorems, with the associated spectral calibration only C1.

The H7 hypothesis is not that coverage alone solves the physical problem. It is that these exact ingredients admit a **normalized, overlap-consistent, history-uniform gluing theorem** whose loss fits the declared continuous good-channel budget. This remains open.

## Two-center atlas and retained-state setting

Write `U_s = {s exp(A): ||A|| <= pi/2}` for `s in {+1,-1}`. A local center word `sigma` assigns a sign to every charted quotient edge. The atlas must be installed after a boundary-rooted, overlap-consistent forest has fixed the finite quotient coordinates. This order matters: the retained boundary connection is gauge covariant, interior gauge transformations have been removed, and every edge used by a crossing plaquette remains in the retained state. Stage 20 shows that deleting such an edge destroys sufficiency.

For a finite volume and cutoff, let `h` denote a retained boundary history with positive state weight. Let `mu_h` be the normalized nonlinear conditional measure on the interior fiber. Choose a measurable, gauge-covariant partition of unity `w_sigma` subordinate to the center-word charts. The chart mass is

```text
p_sigma(h) = integral w_sigma d mu_h,
```

and, when this is positive, the normalized chart conditional is

```text
d mu_{sigma,h} = w_sigma d mu_h / p_sigma(h).
```

This normalization is indispensable. An unnormalized numerator estimate does not control a conditional law when `p_sigma(h)` is small. On a chart, `mu_{sigma,h}` should be compared with a correspondingly normalized Gaussian/reference conditional `nu_{sigma,h}`. Stage 17 gives the correct form of the comparison: a remainder oscillation `kappa` produces an `exp(kappa)` density loss, while the reference chart mass enters through its own normalization. Stage 22 supplies the local nonlinear coercivity and fiber contraction needed at `r_*`; it does not supply this normalized comparison.

## Overlap cocycle and global gluing

On every nonempty chart overlap, coordinate changes must preserve the same quotient-edge configuration and retained history. The local reconstructed measures must obey the exact cocycle identity obtained by changing coordinates, including the Haar Jacobian and partition weights. On triple overlaps the transition factors must multiply to one. For the two-center one-link atlas, multiplicity is at most two, but product charts and adjacent blocks still require a compositional cocycle statement.

If the cocycle holds, gluing is not an approximation:

```text
mu_h(A) = sum_sigma p_sigma(h) mu_{sigma,h}(A)
```

for every measurable fiber event `A`. Approximation enters only through chartwise comparison and the decision to isolate an exceptional channel. Thus overlap error, normalization error, and exceptional mass must be reported separately rather than merged into one informal atlas loss.

## Exceptional mass

The two closed radius-`pi/2` charts have no uncovered group points. Nevertheless, an exceptional channel is still necessary for estimates: it contains configurations outside the small local typical sets, a chosen collar around chart cuts where stable center selection or transition estimates are unavailable, and any center-word sector not yet controlled by the normalized reference comparison. Its conditional mass is

```text
epsilon_exc(h) = mu_h(E_exc).
```

The required quantity is `sup_h epsilon_exc(h)`, also uniform in volume and cutoff. Haar coverage, bounded chart multiplicity, and a finite Jacobian ratio do not bound this conditional probability. Nor may a cut be discarded merely because it has zero Haar measure: positive-mass boundary histories can force conditional laws arbitrarily close to it. Stage 21's dependency-safe Gaussian union bound and Stage 22's local window identify the right finite-scale typical radius, but a physical conditional charge remains to be proved.

## Exact first physical theorem

The first physical H7 theorem should be frozen as follows.

**H7-PT1 (uniform normalized atlas reconstruction).** There exist constants `kappa_* < infinity` and `epsilon_* < 1`, satisfying the declared continuous-channel loss budget and independent of finite volume, cutoff, and retained history, such that for every positive-mass retained history `h`:

1. an overlap-consistent boundary-rooted quotient atlas and gauge-covariant subordinate weights exist;
2. all positive-mass chart conditionals and their reference conditionals are normalized, and on the local good set at radius `r_*` their Radon--Nikodym ratios have logarithmic oscillation at most `kappa_*`;
3. the transition densities satisfy the exact overlap cocycle, so the local laws reconstruct one global conditional law;
4. the exceptional conditional mass is at most `epsilon_*`; and
5. consequently, for every measurable event `A`,

```text
mu_h(A) <= exp(kappa_*) nu_h(A) + epsilon_*.
```

Here `nu_h` is the globally glued normalized reference law, not an unnormalized chart numerator. A usable version must state the numerical budget that `exp(kappa_*)` and `epsilon_*` must meet when inserted into the larger weighted-kernel ceiling. Proving H7-PT1 is the first point at which H7 becomes a physical, history-uniform theorem rather than an atlas probe.

## Falsification program

H7 fails in its intended form if any of the following finite countertests succeeds:

- a single principal `+I` chart is claimed to cover `-I` or to retain bounded logarithmic coordinates globally;
- two adjacent block forests induce incompatible coordinates for a shared retained edge or crossing plaquette;
- normalized chart conditionals disagree on an overlap after the full Jacobian and partition weights are included;
- chart masses become arbitrarily small along positive-mass histories while an unnormalized numerator bound remains fixed;
- `sup_h epsilon_exc(h)` approaches one, even though unconditional exceptional probability is small;
- the Stage 22 coercivity or contraction margin fails before `r_*` under the actual conditional covariance or quotient geometry;
- chartwise constants grow with the number of links, atlas center words, volume, cutoff removal, or history length.

The strongest immediate stress test is an adversarial retained-history table on two overlapping finite blocks: enumerate center words, normalize every nonzero chart fiber, verify pair and triple cocycles, and maximize exceptional charge and density oscillation over histories. Failure localizes H7 before any RG or continuum claim.

## Claim guardrails

The exact group atlas, Haar bounds, quotient disintegration, and sharp finite overlap window remain C2. Numerical tests of particular blocks or history tables are C1. H7-PT1 would be a C2 physical conditional theorem only after all stated uniform quantifiers are proved. It would not by itself establish a volume-uniform bad-kernel ceiling, RG iteration, continuum construction, Osterwalder--Schrader reconstruction, or a Hamiltonian mass gap; those require separate downstream theorems and cannot be labeled C3 from this stream.
