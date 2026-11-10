# Stage 53 -- H1 vacuum-weight duality

This stage develops H1 end to end at the strongest defensible finite and
conditional level.

## Central correction

The vacuum eigenfunction and the forward exploration weight have opposite
orientations:

```text
T psi = lambda psi                       vacuum transfer amplitude
P_ij = T_ij psi_j/(lambda psi_i)         Doob-normalized dynamics
V_i proportional to 1/psi_i              forward rare-state cost weight
```

For a masked bad kernel `Q = M*P`, this gives the exact identity

```text
(Q V)_i / V_i = sum_j M_ij T_ij / lambda.
```

Separately, the Perron vector of a fixed bad subkernel minimizes the positive
weighted ceiling. It is a Lyapunov weight, not automatically a physical
vacuum wavefunction.

## Outputs

- `main.tex` and `h1_vacuum_weight_duality.pdf`: theorem note and frontier
  audit.
- `h1_vacuum_weight.py`: transfer, Doob, Perron, chain, cluster, and hostile
  certificates.
- `h1_vacuum_weight_results.json`: canonical output.
- `test_h1_vacuum_weight.py`: fifteen dependency-free tests.
- `H1_END_TO_END_TODOS.md`: completed finite/conditional work.
- `H1_YM_HANDOFF_TODOS.md`: open physical Yang--Mills obligations.
- `H1_FRONTIER_LEDGER.md`: claim-level ledger.
- `theorem_dependencies_h1.json`: machine-readable theorem graph.

## Strongest result

The four-channel star weight already used in the package is exactly
Perron-optimal. Its weighted ceiling is
`0.002430277501841998`, its scalar row ceiling is one, and its degree-18
branching ratio is `0.8702225337961371 < 1`.

## Claim ceiling

C2 finite positive-transfer and state-weighted-kernel theorems. The complete
normalized nonlinear SU(2) kernel, a physical vacuum identification, uniform
root moments, basin entry, repeated RG, continuum construction, and mass gap
remain open.

## Reproduce

```bash
python3 h1_vacuum_weight.py --write
python3 -m unittest -v test_h1_vacuum_weight.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
