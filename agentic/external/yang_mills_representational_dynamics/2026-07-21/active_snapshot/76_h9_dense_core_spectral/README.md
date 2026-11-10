# Stage 76 — H9 dense-core spectral transfer

This directory develops the immediate finite H9 target at claim level C2. It
separates the true Hamiltonian gap from the gap visible to an observable-
generated invariant subspace, proves the finite density/rank criterion, and
checks the norm-compatible extension from dense core decay to the full
vacuum-orthogonal operator norm.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_dense_core_spectral.py
python3 dense_core_spectral.py --write dense_core_spectral_results.json
python3 -m json.tool dense_core_spectral_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h9_dense_core.json >/dev/null
```

The verified run contains 20 tests. It requires Python 3.11 or newer and
NumPy.

## Files

- `dense_core_spectral.py` — finite Hamiltonian, transfer, density-rank,
  bilinear-decay, hidden-mode, multiplicity, and physical-time certificates.
- `test_dense_core_spectral.py` — positive and hostile tests.
- `dense_core_spectral_results.json` — canonical machine-readable results.
- `theorem_dependencies_h9_dense_core.json` — finite proof and open physical
  dependency graph.
- `RESULT_LEDGER.md` — theorem, proof, counterexamples, and frontier audit.
- `NEXT_STEP_TODOS.md` — OS-density, uniform-decay, and theory-identity handoff.

## Strongest conclusion

For a declared finite positive self-adjoint Hamiltonian, the spectral closure
of centered probes is dense in the vacuum-orthogonal space exactly when its
per-eigenspace visible ranks sum to the full vacuum-orthogonal dimension. A
norm-compatible (e^{-mt}) bilinear estimate then extends to the full
operator norm. Without this rank condition, only the named invariant
subspace is certified.

The (H=\operatorname{diag}(0,0.4,1.2)) fixture reports visible gap (1.2)
from a probe that misses the true (0.4) mode. The cutoff family
(T_a=\operatorname{diag}(1,e^{-a^2})) shows that positive per-step decay can
still have physical-time gap tending to zero.

## First open physical implication

Construct the OS physical Hilbert space and prove that a named gauge-invariant
temporal core is dense and state-separating in its quotient norm, while its
connected correlations obey a uniform positive decay rate in physical time.
Continuum theory identity and the Yang--Mills mass gap remain open.
