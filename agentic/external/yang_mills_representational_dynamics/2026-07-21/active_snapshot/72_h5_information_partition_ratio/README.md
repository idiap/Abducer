# Stage 72 — H5 information and partition-ratio core

This stage makes the finite core of H5 executable. It proves the event-KL
variational identity, checks deterministic data processing, records the exact
normalized bad/good partition-ratio equivalence, and proves KL tensorization
for a finite product reference measure. It also supplies two normalization
counterexamples and a full-support correlated block family for which the
largest possible constant in the proposed local-KL-sum inequality tends to
zero.

The identities are exact mathematics, but the executable KL and ratio
certificates use binary floating point. The common-bit family stores
`log(epsilon)=-n^2`, preserving its mathematical full-support statement even
when the float encoding of `exp(-n^2)` underflows.

The positive separated-block theorem is therefore explicitly a product-model
theorem. No quasi-factorization for the interacting, gauge-constrained,
nonlinear Yang--Mills measure is claimed.

## Reproduce

```bash
python3 -m unittest -v test_h5_information_partition_ratio.py
python3 h5_information_partition_ratio.py --write h5_information_partition_ratio_results.json
python3 -m json.tool h5_information_partition_ratio_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h5_next.json >/dev/null
```

## Artifacts

- `h5_information_partition_ratio.py`: theorem and counterexample code.
- `test_h5_information_partition_ratio.py`: hostile finite tests.
- `h5_information_partition_ratio_results.json`: canonical calibration.
- `theorem_dependencies_h5_next.json`: proof and frontier dependency graph.
- `RESULT_LEDGER.md`: algebraic claims, numerical certificates, obstructions,
  and claim levels.
- `NEXT_STEP_TODOS.md`: completed finite work and open physical obligations.

Strongest status: C1 for the general finite identities and counterexamples;
C2 only for the restricted finite-product tensorization theorem.
