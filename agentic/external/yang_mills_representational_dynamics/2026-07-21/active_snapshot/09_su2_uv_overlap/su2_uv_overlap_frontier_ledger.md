# Stage 09 Frontier Ledger

## Strongest result

The local nonlinear action bounds and a probabilistically small ultraviolet
defect benchmark are not intrinsically scale-incompatible.  The explicit
witness

```text
t=3e-6, r=0.0041, rho=0.0082, r_F=1e-5, Delta=8, alpha=0.1
```

satisfies the following strict inequalities after adding the exponential-link
Haar Jacobian:

| Quantity | Certified value | Required |
|---|---:|---:|
| nonlinear physical singular value | 1.332871 | `> 0` |
| augmented Hessian remainder | 0.968683 | `< 1` |
| centered fiber transport | 0.003941 | `< 1` |
| generated reference-base margin | 0.060732 | `> 0` |
| standalone one-plaquette tail upper | 0.0000551231 | calibration |
| 216-plaquette block union upper | 0.0119066 | calibration |
| weighted branching proxy | 0.842163 | `< 1` |
| rooted weighted activity sum upper | 0.0833694 | `< 1` |

Because every pass condition is strict and the defining functions are
continuous at the witness, the pass set contains a nonempty open parameter
neighborhood.

## Claim audit

| ID | Statement | Status | Level |
|---|---|---|---|
| U1 | Poisson-image standalone tail upper bound | proved | C2 |
| U2 | local Haar-Jacobian derivative bounds | proved | C2 |
| U3 | independent rooted weighted-polymer sum | proved under independence | C2 |
| U4 | strict coexistence witness | proved as a benchmark | C2 |
| U5 | same tail for a plaquette marginal of the full 4D link measure | open | frontier |
| U6 | dependent block/polymer activity estimate | open | frontier |
| U7 | uniform repeated RG to finite physical scale | open | frontier |
| U8 | continuum construction and OS mass gap | open | Clay frontier |

## What changed strategically

Stage 08 showed failure at `t=0.01`; it did not show that every UV scale fails.
Stage 09 identifies the relevant dimensionless separation
`rho/sqrt(t)`.  At the witness it is approximately `4.734`, while the
nonlinear geometry still has a positive margin.  Thus the immediate target is
no longer to enlarge the local chart blindly.  It is to prove that the
complete weak-coupling link measure inherits a comparable block-activity
bound despite shared links, constraints, and topology.

## First unproved implication

Prove, for a gauge-invariant block event `B_X` defined by curvature-chart
failure and for the actual regulated link measure `mu_{t,L}`, an estimate of
the form

```text
sup_L sup_x sum_{X containing x} exp(alpha |X|) |z_{t,L}(X)| < 1
```

in a parameter window that also satisfies the local-action inequalities.  The
activity `z_{t,L}(X)` must include gauge-orbit Jacobians, shared-link
dependence, Bianchi constraints, boundary holonomy, center flux, and all
topological sectors retained by the regulator.

## Mandatory downgrade language

This stage proves a restricted UV overlap benchmark.  It does not prove a
probability tail or polymer expansion for the full four-dimensional
Yang--Mills measure, does not iterate an RG map, does not construct the
continuum theory, and does not imply a Hamiltonian mass gap.

