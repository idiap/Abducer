# Stage 11 Frontier Ledger

## Proved theorem

Let `m` conditional staples lie in a common bi-invariant `SU(2)` ball of
radius `eta`.  For a target curvature radius `rho`, the conditional heat-kernel
energy has bad-event gap at least

```text
rho^2 - m eta^2.
```

Thus `eta<rho/sqrt(m)` gives uniform small-time exponential concentration for
every fixed target plaquette and for their finite union.  The condition is
gauge covariant because simultaneous endpoint gauge transformations preserve
the common-ball radius.

## Frozen calibration

| Parameter | Value |
|---|---:|
| `m` | 6 |
| `rho` | 0.0082 |
| `eta` | 0.001 |
| threshold `rho/sqrt(m)` | 0.00334763598 |
| rate-gap lower bound | 0.00006124 |
| `gap/(2t)` at `t=3e-6` | 10.2066667 |
| small-time proxy | 0.0000369233 |

The `{I,-I}` Stage 10 boundary requires coherence radius `pi/2`, so it is not
admitted by this collar.

## Status matrix

| Claim | Status |
|---|---|
| gauge-covariant coherence definition | proved |
| energy comparison | proved |
| uniform small-time rate gap under the collar | proved |
| finite-time prefactor uniform through repeated RG | open |
| probability/activity of collar failure | open in Stage 11 |
| complete nonlinear link-measure polymer theorem | open |

Strongest level: `C2`.  The theorem validates good-collar conditioning as a
mechanism but does not supply full-measure control.

