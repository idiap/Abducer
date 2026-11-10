# Reproducibility

Requirements:

- Python 3.10 or later;
- a TeX distribution containing `latexmk`, `pdflatex`, `amsmath`, `amsthm`,
  `mathtools`, `hyperref`, `booktabs`, and the other standard packages named in
  the sources.

No third-party Python packages are required.

## Compile the conceptual documents

From `01_conceptual_foundations`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error generative_relational_coherence_universe.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error phenomenon_preserving_representations_yang_mills.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error yang_mills_mass_gap_conceptual_difficulty.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error yang_mills_relational_rigidity_clay_program.tex
```

## Relational-rigidity programme

From `02_relational_rigidity_program`:

```bash
python3 -m unittest -v test_finite_spectral_core.py
latexmk -pdf -interaction=nonstopmode -halt-on-error ym_relational_rigidity_program.tex
```

Expected: 9 tests pass.

## Heat-kernel basin-entry attack

From `03_heat_kernel_basin_entry`:

```bash
python3 -m unittest -v test_heat_kernel_influence.py test_advanced_regulator_calibration.py
python3 heat_kernel_influence.py --output json
python3 advanced_regulator_calibration.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error heat_kernel_basin_entry_attack.tex
```

Expected: 14 tests pass.

## Fibered block-RG attack

From `04_fibered_block_rg`:

```bash
python3 -m unittest -v test_two_plaquette_bridge.py
python3 two_plaquette_bridge.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error fibered_block_rg_theorem.tex
```

Expected: 8 tests pass.

## Verify package integrity

From the package root:

```bash
sha256sum -c CHECKSUMS.sha256
```

