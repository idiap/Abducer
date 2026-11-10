# Nonlinear Transfer Ten-Phase Synthesis

Date: 21 July 2026  
Stages: 41--50  
Claim level: C2

## Main outcome

The run selects the normalized comparison route over the local repair route.
On the certified convex `SU(2)` chart, nonlinear Fréchet dispersion admits an
exact gauge-invariant inclusion into the dependent Gaussian quadratic form.
With the frozen centered-reference density and complement constants, the
complete low/high continuous row is

```text
7.757562504510382e-05
```

against an allocated continuous budget

```text
9.721110007367992e-04.
```

The numerical margin is strict. The physical theorem remains conditional on
two uniform premises for every positive-mass retained history `h`:

```text
mu_h(A intersect G_h) <= exp(ell_h) nu_h(A intersect G_h)
mu_h(G_h^c) <= q_exc,h.
```

Together they must give

```text
q_low,h + exp(ell_h) q_gauss,h + q_exc,h
    <= 0.0009721110007367992.
```

## Exact nonlinear geometry

If the staples lie in a radius-`r` ball about their Fréchet mean and satisfy
the Karcher equation, the pairwise proxy `P` and Fréchet dispersion `D` obey

\[
  \left(\frac{\sin r}{r}\right)^2D\le P\le D.
\]

At the certified staple radius `0.010432415344772867`, the squared metric
factor is `0.9999637220964704`. The three-link logarithmic Taylor remainder
per staple is `0.0003316872463131322`. At nonlinear RMS threshold `0.006`,
the effective Gaussian threshold remains `0.0056682039189891965`, safely
inside the Stage 35 window.

## Why the repair route fails

The centered tangent-star contraction is initially attractive. It includes
all fifteen Jacobian dimensions and has ideal free energy
`14.23692824618157`, above the channel target. But the staple coordinates are
not independent physical variables.

The exact minimum external-curvature spectrum of a link lift is

```text
0
1.121212121212
1.121212121212
1.635983263598
1.635983263598
```

for every one of the eight interior links. Four centered modes necessarily
export curvature outside the repaired star. The worst-mode lifted free energy
is `-15.898418928673726`; hence the generic single-star repair is falsified
even under the favorable assumption of zero initial external curvature.

A coordinated polymer repair would be sufficient if its effective spill
coefficient were at most `0.9683231479404556` at the upper split, compared with
the measured single-star value `1.635983263598`. This is a backup design target,
not a constructed repair.

## Sector advances

For periodic `GF(2)` center flux, a sector with Hamming label weight `k` has
exact minimum plaquette weight `4k`. Across the 64 sectors the weights
`0,4,8,12,16,20,24` occur with multiplicities
`1,6,15,20,15,6,1`.

Center labels remain incomplete. Integral fluxes

```text
(2k,0,0,0,0,2k)
```

have the same zero center label but Pfaffian charge `4k^2`. The retained state
must therefore include an integer flux lift. Full nonabelian second-Chern
control and uniform integer-sector weights remain open.

## Updated residual budget

After subtracting the restricted continuous row, the remaining target is
`0.002352701876796894`. Equal allocation among center, cut/orbit, and integer
topology gives ceiling `0.000784233958932298` and free-energy target
`7.1508031651258825` for each channel before channel-specific losses.

## Ranked next targets

1. Prove the boundary-uniform normalized density comparison and nonlinear
   chart-complement estimate. This is the primary route.
2. Construct a coordinated polymer repair only as an independent backup.
3. Turn center minimum barriers into full sector partition-ratio bounds.
4. Bound cut/orbit transitions on a complete retained atlas.
5. Construct nonabelian integer topology and uniform sector weights.
6. Only then attempt physical one-scale basin entry and repeated RG.

## What remains unproved

- the physical nonlinear continuous-channel bound;
- the complete multichannel one-scale ratio;
- volume-uniform basin entry;
- a repeated gauge-covariant RG trajectory;
- continuum Yang--Mills construction and Osterwalder--Schrader reconstruction;
- a positive Hamiltonian mass gap.
