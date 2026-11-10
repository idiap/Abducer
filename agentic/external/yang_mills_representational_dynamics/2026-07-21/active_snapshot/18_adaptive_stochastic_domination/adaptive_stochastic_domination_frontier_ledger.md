# Stage 18 Frontier Ledger

## Exact theorem

For an ordered Boolean field, assume every positive-probability history obeys

```text
P(X_i=1 | X_1,...,X_{i-1}) <= q_i.
```

Using common independent uniforms at each exposure step constructs
`X_i<=Y_i` almost surely with independent `Y_i~Bernoulli(q_i)`.  This is a
valid stochastic-domination route and does not require Mayer/Ursell activity
identification.

## Moment-only failure

The law `P(10)=P(01)=1/2` obeys all intersection bounds at `q=1/2`, including
`P(11)=0<=1/4`.  Nevertheless `P(X_1 or X_2)=1>3/4`, and the conditional
probability of the second bit after history `X_1=0` is one.  Thus Stages 13--14
event moments alone cannot justify domination.

## Stage 14 budget

| Quantity | Value |
|---|---:|
| effective conditional target `q_eff` | `0.00243027750` |
| critical degree-18 weight | `0.00279270808` |
| branching ratio | `0.870222534` |
| rooted connected sum | `0.0206959813` |

The abstract conversion closes if the adaptive premise is established.

## Corrected frontier

Construct a multi-link/block exposure for the complete `SU(2)` measure and
prove the stated bound after every positive history, uniformly in volume.
