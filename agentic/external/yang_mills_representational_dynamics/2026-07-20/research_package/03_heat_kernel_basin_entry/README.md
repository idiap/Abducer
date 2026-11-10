# Heat-kernel basin-entry attack

This package implements the first theorem-level follow-up to the relational
rigidity programme.

## Main result

The naive worst-case total-variation Dobrushin coefficient is not uniform in
the small heat-time limit.  On every nontrivial compact group, a heat kernel
converges to a point mass at the identity while a fixed translate converges to
a different point mass, so their total-variation distance tends to one.

This falsifies the original single-scale worst-case basin as a plausible
continuum entry criterion.  The paper replaces it with a two-tier local basin:
contractive couplings on a gauge-invariant good-field region plus a summable
defect-disagreement matrix.

## Files

- `heat_kernel_basin_entry_attack.tex` and `.pdf`: complete follow-up paper.
- `heat_kernel_influence.py`: U(1) heat-kernel influence calibration.
- `test_heat_kernel_influence.py`: adversarial unit tests.
- `advanced_regulator_calibration.py`: SU(2), blocking, defect-tail, and
  heat-kernel/Wilson diagnostics.
- `test_advanced_regulator_calibration.py`: advanced calibration tests.
- `calibration.json`: reproducible numerical results.
- `advanced_calibration.json`: reproducible advanced results.
- `next_step_ledger.md`: proved, conditional, falsified, and open claims.

## Reproduce

```bash
python3 -m unittest -v test_heat_kernel_influence.py
python3 -m unittest -v test_advanced_regulator_calibration.py
python3 heat_kernel_influence.py --output json > calibration.json
python3 advanced_regulator_calibration.py --output json > advanced_calibration.json
latexmk -pdf -interaction=nonstopmode -halt-on-error heat_kernel_basin_entry_attack.tex
```

The numerical output illustrates the theorem; it is not used as its proof.
