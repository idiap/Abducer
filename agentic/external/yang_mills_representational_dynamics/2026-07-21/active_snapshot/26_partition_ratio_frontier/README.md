# Stage 26: Conditional Partition-Ratio Frontier

This stage writes the nonlinear retained-state problem as an exact partition
ratio.  For good partition `Z_G(s)`, bad partition `Z_B(s)`, weighted bad
numerator `B_V(s)`, and current state weight `V(s)`, the bad row is

```text
B_V(s)/((Z_G(s)+Z_B(s))V(s)).
```

A free-energy charge `F` relative to a good reference, together with good
comparison loss `ell`, yields the ceiling `exp(ell-F)`.  The residual budget
requires `F>6.71292101139`.  This inequality is not yet proved uniformly for
the physical nonlinear measure.

```bash
python3 -m unittest -v test_partition_ratio_frontier.py
python3 partition_ratio_frontier.py --output json
```
