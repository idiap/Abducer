# H7 Stage 74 result ledger

## Proved at C2: exact finite theorem

### H7-F1: two-center cover and positive subordinate weights

The finite `+I`/`-I` carrier is covered exactly, no point has chart
multiplicity above two, and every active partition weight is strictly
positive.  The partition sums to one at every carrier point.

### H7-F2: normalized global gluing

For every strictly positive probability `mu` on the carrier, the chart masses
and chart laws

```text
p_s = sum_x mu(x)w_s(x),
mu_s(x) = mu(x)w_s(x)/p_s
```

are normalized and satisfy

```text
mu(A) = sum_s p_s mu_s(A)
```

for every event.  The executable certificate exhausts all 64 events and has
exact residual zero.

### H7-F3: full normalized overlap cocycle

Relative to chart coordinate carriers `kappa_s`, with
`J_{s,t}=d kappa_t/d kappa_s`, the conditional densities obey

```text
f_t = [(w_t/w_s)(p_s/p_t)/J_{s,t}] f_s.
```

Both density residuals and the forward/reverse cocycle residuals vanish
exactly on both overlap atoms.  The Jacobians `3/2` and `2/5` are nontrivial.

### H7-F4: exact exceptional-channel decomposition

Removing the declared exceptional atom from the regular chart channels and
normalizing all three surviving channels gives an exact convex decomposition
of the original law.  All 64 event identities again have exact residual zero.

### H7-F5: adjacent-block overlap consistency

On a shared retained equator edge, opposite center charts reconstruct the same
quaternion from distinct signed half-turn coordinates. Applying the declared
chart center gives exact agreement, while a same-sign minus-chart perturbation
is rejected. The two-step and four-step product-word cocycles equal one for
both overlap atoms.

### H7-F6: hostile-history obstruction

There is an exact family of positive histories with

```text
p_+ = 3/(4n),       raw numerator = 1/(4n),
normalized probability = 1/3.
```

The normalization amplification is `4n/3` and is unbounded.  Another exact
family keeps cover fraction one while exceptional probability `1-1/n` tends
to one.  Therefore neither a raw numerator nor geometric coverage supplies a
history-uniform conditional estimate.

## Claim boundary

The following are **not proved**:

- the full boundary-rooted forest and crossing-plaquette atlas;
- a normalized nonlinear Yang--Mills conditional density comparison;
- a volume-, cutoff-, and history-uniform exceptional bound;
- H7-PT1, RG iteration, continuum construction, OS reconstruction, or a mass
  gap.

The result is C2 because all finite identities are symbolic rational theorems,
not merely numerical probes.  It is not a C2 physical Yang--Mills theorem.
