# Stage 24 Frontier Ledger

## Exact star-weight theorem

For the star subkernel

```text
Q(0,i)=a_i,   Q(i,0)=b_i,   Q(i,i)=c_i,
```

and a target `q>max_i c_i`, set `V(0)=1` and
`V(i)=b_i/(q-c_i)`.  On the charged branch `V(i)>=1`,

```text
QV <= qV  iff  sum_i a_i b_i/(q-c_i) <= q.
```

For four forced-return channels with zero persistence and equal entry rates,
the total entry budget is `q^2=5.90624873596e-6`.  Each entry must therefore
be at most `1.47656218399e-6`, while the stored defect weight is
`1/q=411.47564393`.

## Strategic consequence

State weighting stores a rare-entry cost; it does not eliminate it.  With a
forced following bad transition, a weighted ceiling `q` requires total entry
probability of order `q^2`.  Any persistence channel must itself be below
`q`.

## Open

No uniform physical `SU(2)` bounds on `a_i,b_i,c_i` have been established.
The local boundary representation carries center and orbit labels but not a
genuine topology sector.  Strongest level: `C2` exact finite-kernel theorem.
