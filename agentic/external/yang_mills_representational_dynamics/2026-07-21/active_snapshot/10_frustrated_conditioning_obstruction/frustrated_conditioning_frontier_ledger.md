# Stage 10 Frontier Ledger

## Strongest result

The side-two four-dimensional `SU(2)` block admits a realizable microscopic
conditioning under which an interior link has five identity staples and one
negative-center staple.  The exact conditional density is

```text
gamma_t(dU) proportional to p_t(U)^5 p_t(-U) dU.
```

Its small-time class-angle rate function is

```text
I_6(theta) = 5 theta^2 + (pi-theta)^2.
```

The unique minimizer and target curvature are

```text
theta_* = pi/6,
theta_target(theta_*) = 5pi/6.
```

For a target good radius `rho<5pi/6`,

```text
lim_{t->0} 2t log P(target good | frustrated conditioning)
  = -6(5pi/6-rho)^2.
```

At the Stage 09 radius `rho=0.0082`, the positive rate gap is
`40.8661445`.  Therefore the target plaquette is conditionally bad with
probability tending to one.

## Claim audit

| ID | Claim | Status | Level |
|---|---|---|---|
| F1 | degree-six interior-link incidence | proved exactly | C2 |
| F2 | center-staple map has GF(2) rank six | proved exactly | C2 |
| F3 | conditional density is `p_t(U)^5p_t(-U)` | proved | C2 |
| F4 | exact rate minimizer and good-event gap | proved | C2 |
| F5 | worst-case microscopic uniform-tail route fails | proved | C2 |
| R1 | same obstruction defeats good-collar conditioning | not claimed | open |
| R2 | contour activity charges every frustration | open | frontier |
| R3 | volume-uniform dependent polymer sum | open | frontier |
| R4 | repeated RG, continuum theory, and gap | open | Clay frontier |

## Quantifiers ruled out

The theorem rules out an estimate of the form

```text
sup_{all surrounding link conditionings omega}
  P_t(plaquette p is bad | omega) <= epsilon(t),
epsilon(t) -> 0.
```

Indeed the supremum tends to one.  By continuity of the conditional density,
the obstruction persists in a neighborhood of the exact center-valued
conditioning; it is not merely an undefined measure-zero conditional value.

## Quantifiers not ruled out

The theorem does not rule out:

- conditioning only on a quantitatively good collar;
- averaging over the boundary distribution induced by the full measure;
- integrating all links in a block before assigning an activity;
- charging a frustrated boundary to the same connected polymer;
- separate center-flux or topological polymer species.

## Strategic consequence

The Stage 09 one-plaquette tail cannot be lifted to the interacting measure by
a naive supremum over local conditionings.  The next theorem must preserve the
energetic cost of the conditioning.  A contour or polymer cannot treat the
external frustration as free data; it must include it in the activity support
and pay its action/entropy cost.

## Mandatory downgrade language

This is a restricted finite-block obstruction theorem.  It eliminates one
proof mechanism; it does not eliminate constructive RG, prove the required
dependent activity bound, construct continuum Yang--Mills, or establish a
mass gap.

