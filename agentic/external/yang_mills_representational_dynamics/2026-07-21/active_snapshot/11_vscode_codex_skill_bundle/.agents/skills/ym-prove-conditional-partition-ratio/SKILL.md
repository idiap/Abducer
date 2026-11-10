---
name: ym-prove-conditional-partition-ratio
description: Reduce finite-volume nonlinear Yang--Mills conditional estimates to exact good/bad weighted partition ratios, derive the required uniform free-energy inequality, and falsify action-only or boundary-nonuniform arguments. Use when a retained-state, large-field, exceptional-block, or state-weighted defect claim must be connected to a one-scale K+R basin bound without assuming independence, a pre-existing gap, or uncontrolled normalizers.
---

# Prove a Conditional Partition-Ratio Bound

## Freeze the conditional object

1. Declare the regulator, finite volume, boundary conditions, block exposure,
   retained state `s`, compact conditional fiber, and positive fiber weight
   `w_s(f)`.
2. Declare a measurable good/bad split and the next-state map `tau(s,f)`.
3. Require every supremum to range only over positive-mass retained histories,
   but over all such histories uniformly in volume.

## Use the exact reduction

Define

```text
Z_G(s) = integral_G w_s,
Z_B(s) = integral_B w_s,
B_V(s) = integral_B w_s(f) V(tau(s,f)).
```

The weighted bad row is exactly

```text
q_V(s) = B_V(s)/((Z_G(s)+Z_B(s))V(s)).
```

Do not replace the full normalizer by an unproved constant.  A sufficient
free-energy route is

```text
Z_G(s) >= exp(-ell) Z_G_ref(s),
B_V(s) <= exp(-F) Z_G_ref(s)V(s),
```

which gives `q_V(s) <= exp(ell-F)`.  For target `q`, require strictly
`F > ell-log(q)`.

## Compose with the good channel

When a comparison-controlled subkernel `K` and charged residual `R` are used,
prove each premise separately:

```text
K <= exp(ell) K0,
K0 V <= kV,
R V <= rV.
```

Then `(K+R)V <= (exp(ell)k+r)V`.  Check the declared connected-set threshold,
including adjacency degree and activity weight, before calling the one-scale
bound subcritical.

## Mandatory falsifications

- Multiply individually charged bad configurations by exponential
  multiplicity; action charge without entropy need not suppress `Z_B`.
- Let `Z_G(s)` collapse along retained states; pointwise local formulas do not
  imply a uniform conditional comparison.
- Test defect persistence at or above the proposed weighted ceiling.
- Test omitted center, cut-locus/orbit, and topology labels.
- Test zero-mass histories, invalid weights, volume-dependent constants, and
  equality at a threshold that requires strictness.

## Evidence and stop conditions

Return the conditional-kernel schema, exact ratio identity, good comparison
loss, charged numerator inequality, state weight, threshold arithmetic,
counterexamples, dependency graph, and first unproved supremum inequality.

Label the physical one-scale result open unless the numerator and normalizer
bounds hold for the complete nonlinear measure uniformly over finite volumes
and retained states.  Do not infer repeated RG, continuum construction,
Osterwalder--Schrader reconstruction, or a Hamiltonian mass gap from a finite
partition-ratio theorem.
