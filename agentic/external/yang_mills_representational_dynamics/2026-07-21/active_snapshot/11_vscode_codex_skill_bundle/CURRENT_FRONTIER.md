# Current Yang--Mills workflow frontier

H1--H10 parallel-execution update (21 July 2026): Stages 68--77 execute the
next falsification target in every independent hypothesis stream and pass
194/194 tests after audit repairs.  The most decisive new result is negative:
for `T_delta=[[1,delta],[delta,1]]`, the same positive transfer supplies the
Gibbs weight, Perron vacuum, Doob kernel, and masked bad subkernel, while both
the weighted bad ceiling and temporal gap tend to zero.  Thus same-measure
calibration alone does not bridge defect rarity to spectral rigidity.  Exact
finite results now also cover multistar spectra, the six-flux topology
carrier, typed recovered squares, normalized signed-chart gluing, stable
state refinement, multiplicity-sensitive spectral density, and finite
observable recovery.  Their shared first blocker is still the physical
normalized nonlinear `SU(2)` retained-state conditional kernel; full-spectrum
observability/coercivity is an independent second gate.  See Stages 78--79 for
the conservative audit and reward-ranked continuation.

Five-target H1 downstream update (21 July 2026): Stages 54--58 construct the
exact finite normalized conditional kernel, prove an entrywise Harnack/root
moment criterion, establish robust multichannel Perron envelopes, prove the
changing-state-space weight cocycle, and audit the basin/OS handoff.  The
four-channel envelope has additive weighted slack
`0.0003624305785159018`, relative multiplicative slack
`0.1491313556748981`, and symmetric persistence/tunneling budget
`0.0006792623948561134`.  Two decisive corrections follow.  Constant
contraction per geometrically growing RG level is power-law in terminal scale,
not exponential in physical distance; and a fixed spatial one-scale ceiling
is compatible with positive temporal transfer matrices whose gaps tend to
zero.  The run contributes 52 passing tests and five clean theorem notes.  Its
strongest level is C2 with C3 conditional bridges, not physical basin entry.

H1 end-to-end update (21 July 2026): Stage 53 corrects and completes the finite
vacuum-weight mechanism.  For a positive temporal transfer amplitude
`T psi = lambda psi`, the Doob kernel is
`P_ij=T_ij psi_j/(lambda psi_i)`, but the natural forward rare-state cost is
`V_i proportional to 1/psi_i`.  For a bad-edge mask this orientation cancels
vacuum ratios exactly.  Independently, Collatz--Wielandt shows that the Perron
vector of a fixed bad subkernel is its optimal positive Lyapunov weight; it is
not automatically a physical vacuum amplitude.  The package's four-channel
star weight is exactly Perron-optimal with ceiling
`0.002430277501841998`, scalar ceiling one, and degree-18 branching ratio
`0.8702225337961371`.  Fifteen hostile tests pass.  The claim ceiling is C2:
the complete normalized nonlinear SU(2) kernel, its reflection-compatible
vacuum identification, and uniform inverse-weight/root-moment bounds remain
open in `53_h1_vacuum_weight/`.

Conceptual-restrategy update (21 July 2026): Stage 52 selects a
vacuum-weighted, normalized, multichannel retained-state kernel inequality as
the highest-reward primary target.  First probes of ten aggressive hypotheses
are stored in `52_conceptual_restrategy/`.  The multi-star linear diagnostic
finds four zero-spill directions for the central four-link system and seven
for all eight interior links, while the orientation-correct one-star system
still has none; no polymer boundary law follows.  An exact integral-flux
collision proves that center labels plus total Pfaffian charge are not
compositionally sufficient, so the retained topology must include the full
integer flux lift or equivalent bilinear data.  These are C1/C2 diagnostics,
not physical basin entry.

Publication update (21 July 2026): the orientation-correct single-star
calculation is now isolated as Paper 05.  On the open side-two four-cube, the
centered Gaussian star covariance spectrum is
`0, 239/630 (x2), 33/70 (x3)`, while the exact minimum external-curvature lift
spectrum is strictly positive: `37/33 (x3), 391/239 (x2)`.  The earlier
zero-spill mode came from centering signed plaquette rows before putting them
in the common rooted-link orientation.  Use `ym-draft-staple-dispersion` for
this theorem cluster.

Use this file as the starting context for the next Codex run.

## Strongest result

Stages 41--50 transport the exact projected-Gaussian dispersion mechanism
through the certified local `SU(2)` geometry.  If the Karcher mean and all six
staples lie in a geodesic ball of radius `r<pi/2`, the pairwise proxy `P` and
Karcher variance `D` obey

```text
(sin(r)/r)^2 D <= P <= D.
```

At the frozen link radius, the metric factor is `0.9999818608837214`.  The
exact normalized transfer theorem gives

```text
reference tail upper                    1.1225944951196765e-10
comparison log loss                     0.00018100567968280893
chart-complement upper                  7.757522445438629e-05
restricted continuous probability       7.757562504510382e-05
continuous-channel ceiling              0.0009721110007367992
```

Thus the continuous channel closes in the centered retained reference.  This
is a restricted/conditional theorem, not yet a physical boundary-uniform
statement.

## Additional finite interfaces

- The ideal centered tangent repair closes its local free-energy target, but
  the exact minimum-norm link lift has spill coefficient `1.635983263598`,
  above the admissible `0.9683231479404556`.  The generic single-star repair is
  therefore falsified; coordinated polymer repair remains only a backup.
- The positive-mass retained-history interface and its adaptive implication
  are exact once every history row receives density and complement bounds.
- Periodic `GF(2)` flux sector `k` has minimum center-plaquette weight `4k`,
  with exact multiplicities `1,6,15,20,15,6,1`.
- The integral Pfaffian carrier
  `Q=n01*n23-n02*n13+n03*n12` proves that center labels erase unbounded
  integer charge, so center control is not topologically complete.
- After restricted continuous closure, the residual three-channel budget is
  `0.002352701876796894`, or `0.000784233958932298` per equal channel.

## First open physical inequality

Construct the complete normalized nonlinear retained-state bad subkernel
`Q_{a,L}` and a strictly positive physical or exploration-derived cost weight
`V_{a,L}`.  Uniformly over lattice spacing, finite volume, and every
positive-mass retained history, prove

```text
Q_{a,L} V_{a,L} <= q V_{a,L},
root_law_{a,L}(V_{a,L}) <= M,
q < 0.0027927080803578997,
```

where `M` is independent of `a`, `L`, and the retained history.  Construction
of each row still requires the normalized density and chart-complement
comparison from Stage 50; exceptional mass cannot be hidden by erasing
positive-mass histories.  A temporal-vacuum route must identify the row kernel
with the corresponding Doob transform and uses `V=1/psi`.  An exploration
route may use the bad-kernel Perron vector, but cannot call it a physical
vacuum without a separate reflection-positive temporal theorem.

## Next target order

1. Prove the boundary-uniform normalized density and chart-complement
   comparison above.
2. Construct a coordinated polymer repair only as an independent backup.
3. Convert exact center minimum barriers into full sector partition ratios.
4. Bound the cut/orbit channel on a complete retained atlas.
5. Construct nonabelian integer topology and uniform sector weights.
6. Only then claim physical one-scale basin entry and attempt repeated RG.

Use `$ym-prove-conditional-partition-ratio` for normalization,
`$ym-prove-adaptive-block-domination` and
`$ym-prove-state-weighted-defect-transfer` for histories,
`$ym-control-large-fields-and-topology` for sector completeness, and finish
with `$ym-audit-frontier`.

No physical one-scale basin entry, continuum construction, or mass gap is yet
proved.
