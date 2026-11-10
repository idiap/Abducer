# H4 next-step TODOs

## Completed finite periodic baseline

- [x] Implement the exact six-component integer flux carrier.
- [x] Implement mod-two center reduction and exact additive composition.
- [x] Polarize the Pfaffian and certify its unimodular pairing matrix.
- [x] Verify orientation covariance under all 24 coordinate permutations.
- [x] Implement six-context signatures and exact reconstruction of full flux.
- [x] Prove contextual minimality of the full flux/pairing covector.
- [x] Compute the full trivial Smith forms of the one-cell periodic cubical
  four-torus and recover integral Betti numbers ((1,4,6,4,1)).
- [x] Exhaust all 531,441 two-block pairs in \(\{-1,0,1\}^6\).
- [x] Exhibit a scalar sector-weight gluing collision using exact fractions.
- [x] Add hostile validation, algebraic, exhaustive, and fail-closed tests.

## P1b — bounded relative cubical block

- [ ] Freeze a concrete bounded (L^4) cubical block, its oriented cells,
  boundary subcomplex, and gluing interface.
- [ ] Construct all integral boundary and coboundary matrices with incidence
  signs and verify \(\partial^2=0\) exactly.
- [ ] Compute Smith normal forms for the absolute, boundary, and relative
  complexes, including explicit basis transformations and all torsion.
- [ ] Implement the long exact sequence of the pair and identify the kernel
  invisible to absolute bulk flux.
- [ ] Define a cellular cup/intersection product compatible with the chosen
  diagonal approximation and verify orientation reversal.
- [ ] Construct canonical absolute and relative cocycle representatives.
- [ ] Implement the interface restriction and connecting maps.
- [ ] Compare direct two-block relative classification with composition of
  one-block carriers on an exhaustive bounded cocycle catalog.
- [ ] For every failed merge, emit the smallest boundary/transgression
  context that separates it.

**Exit criterion:** a machine-checkable carrier for a bounded block, or a
minimal explicit interface datum whose omission breaks direct-versus-composed
classification.

## P2 — nonabelian topology carrier

- [ ] Freeze the physical theory: gauge group/global form, strict-periodic or
  twisted boundary conditions, lattice action, admissibility condition, and
  boundary gauge group.
- [ ] State and implement the regulator-specific nonabelian topological
  classifier without identifying it with the embedded-abelian Pfaffian.
- [ ] Prove interior gauge invariance and specify boundary gauge covariance.
- [ ] Relate center twist, integer charge, and boundary transgression with all
  convention factors explicit.
- [ ] Define a gauge-invariant exceptional event for chart/admissibility
  failure and bound its normalized mass rather than deleting it.
- [ ] Test torons, twists, instanton-like representatives, orientation
  reversal, and near-admissibility-boundary fields.

## P3 — physical topology-sector kernel

- [ ] Define a boundary-resolved retained state sufficient for gluing.
- [ ] Define all unnormalized topology-sector integrals with one common
  normalization denominator.
- [ ] Prove positivity, row normalization, and sector exhaustiveness.
- [ ] Compare direct two-block integration with composed one-block kernels.
- [ ] Refine the retained state whenever two boundary-conditioned rows differ.
- [ ] Prove a strict topology-channel Lyapunov bound uniformly over retained
  boundary histories and at two successive scales.

## Stop conditions

- [ ] Do not promote the periodic one-cell Smith calculation to a bounded
  relative-block theorem.
- [ ] Do not treat center twist, embedded-abelian flux, and nonabelian second
  Chern data as interchangeable.
- [ ] Do not compose scalar sector weights without boundary response.
- [ ] Do not infer normalized probability suppression from minimum action.
- [ ] Do not claim repeated RG, continuum existence, or a mass gap from this
  finite carrier.

