# Stage 26 Frontier Ledger

## Exact reduction

Let the compact conditional fiber over retained state `s` have positive
weight `w_s`.  With a good/bad split and next-state map `tau`, define

```text
Z_G(s) = integral_G w_s,
Z_B(s) = integral_B w_s,
B_V(s) = integral_B w_s(f) V(tau(s,f)).
```

Then the exact weighted bad row is

```text
B_V(s)/((Z_G(s)+Z_B(s))V(s)).
```

If `Z_G(s)>=exp(-ell) Z_G_ref(s)` and
`B_V(s)<=exp(-F) Z_G_ref(s)V(s)`, it is at most `exp(ell-F)`.
For the Stage 25 residual budget the uniform requirement is

```text
F > 6.71292101139.
```

## Falsification results

An action charge of `10` can be canceled by `22027` bad microstates, giving
bad probability about `0.500006`.  A second counterexample has identical
pointwise good formulas but conditional bad ratios near zero and `1/2` in two
retained states.  Thus entropy and the boundary-state normalizer must both be
controlled.

## First unproved inequality

Uniformly in finite volume, exposure history, positive-mass retained state,
and defect channel, prove

```text
B_V(s)/(Z_G_ref(s)V(s)) <= exp(-F_*),  F_*>6.71292101139.
```

This is the current first physical analytic frontier.  One-scale basin entry,
repeated RG, continuum construction, and the Hamiltonian gap remain open.
Strongest level: `C2` exact reduction theorem.
