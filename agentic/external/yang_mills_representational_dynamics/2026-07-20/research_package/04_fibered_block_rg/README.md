# Fibered two-plaquette block attack

This package implements the next interacting-block phase of the heat-kernel
Yang--Mills programme.

Its central distinction is between:

- the retained coarse holonomy, which transports relevant information and is
  not expected to contract at one RG step; and
- the centered fiber fluctuation, which is integrated out and can contract.

The two-plaquette U(1) heat-kernel bridge shows this explicitly. Its full
internal coordinate has boundary Lipschitz response approaching `1/2`, while
the centered fiber response approaches zero in the Gaussian tangent limit.

## Contents

- `fibered_block_rg_theorem.tex` and `.pdf`: self-contained theorem dossier.
- `two_plaquette_bridge.py`: bridge, circular Wasserstein, defect, and
  regulator-comparison calibrations.
- `test_two_plaquette_bridge.py`: executable tests.
- `fiber_calibration.json`: reproducible results.
- `fibered_frontier_ledger.md`: theorem and open-obligation ledger.

## Reproduce

```bash
python3 -m unittest -v test_two_plaquette_bridge.py
python3 two_plaquette_bridge.py --output json > fiber_calibration.json
latexmk -pdf -interaction=nonstopmode -halt-on-error fibered_block_rg_theorem.tex
```

The compact U(1) computations and Gaussian tangent model are restricted
calibrations. They do not prove four-dimensional Yang--Mills basin entry.
