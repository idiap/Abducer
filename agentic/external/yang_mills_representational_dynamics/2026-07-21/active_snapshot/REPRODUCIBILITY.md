# Reproducibility

Requirements:

- Python 3.10 or later;
- NumPy 2.x for the numerical stages through Stage 50 and SciPy 1.10 or later for the explicit
  `(2^4)` quotient/fiber and high-dimensional chart-mass calibrations;
- a TeX distribution containing `latexmk`, `pdflatex`, `amsmath`, `amsthm`,
  `mathtools`, `hyperref`, `booktabs`, and the other standard packages named in
  the sources.

The first three computational stages use only the Python standard library.
The explicit four-dimensional quotient/fiber stage uses NumPy and SciPy; the
one-step effective-action stage uses NumPy.
The one-plaquette heat-kernel initializer also uses NumPy.
The nonlinear block-geometry stage uses NumPy and imports the adjacent Stage
07 heat-kernel module.
The ultraviolet-overlap stage uses NumPy and imports the adjacent Stage 08
block-geometry module.
The frustrated-conditioning stage uses NumPy for stable log-domain quadrature
and imports the adjacent nonlinear block geometry.
The good-collar stage uses only the standard library.  The center-contour and
dependent-Gaussian stages use NumPy and import the exact block complex from
earlier stages.  The nonlinear-transfer stage uses the standard library
directly and imports the Stage 12 and Stage 13 certificates.
The nonasymptotic collar stage imports the Stage 07 image certificate.  The
continuous-charging stage uses NumPy and the Stage 08 quaternion operations.
The chart-comparison stage uses SciPy's regularized gamma function outside the
deep lower-tail series.  The adaptive-domination stage imports the Stage 14
weight certificate.
The state-weighted stage uses NumPy for finite positive kernels.  The boundary
disintegration stage uses NumPy quaternion arithmetic.  The typical-set stage
uses NumPy and imports the Stage 08 complex and Stage 17 stable Gaussian-ball
routine.  The sharp-overlap stage imports the Stage 07, 08, and 21
certificates.  The local-cylinder stage imports Stages 21 and 22.  The
multichannel-weight stage uses NumPy.  The one-scale `K+R` stage imports
Stages 19, 21, 22, and 23.  The partition-ratio stage uses NumPy and imports
the Stage 25 calibration.
Stages 31--34 use finite metric, incidence, and Gaussian radial calculations;
Stage 35 uses NumPy and the exact projected curvature complex; Stage 36 uses
the Stage 35 tail certificate; Stages 37--38 implement finite weighted
partition identities; Stage 39 uses NumPy elimination over `GF(2)`; and Stage
40 composes the adjacent calibration modules.
Stages 41--42 use NumPy and import the projected-Gaussian and local-chart
certificates.  Stages 43--45 use NumPy linear algebra for the centered repair,
minimum-norm link lift, and coordinated spectral frontier.  Stage 46 composes
the positive-mass history interface; Stage 47 uses exact `GF(2)` enumeration;
Stage 48 uses finite integer-flux enumeration; and Stages 49--50 compose the
new calibration modules.

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

## `SU(2)` quotient/fiber block

From `05_su2_quotient_fiber`:

```bash
python3 -m unittest -v test_su2_block_linearized.py
python3 su2_block_linearized.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_quotient_fiber_theorem.tex
```

Expected: 11 tests pass.

## One-step generated effective action

From `06_one_step_effective_action`:

```bash
python3 -m unittest -v test_one_step_effective_action.py
python3 one_step_effective_action.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error one_step_effective_action_theorem.tex
```

Expected: 12 tests pass.  Across all five computational stages, 54 tests pass.

## `SU(2)` heat-kernel initializer

From `07_su2_heat_kernel_initializer`:

```bash
python3 -m unittest -v test_su2_heat_kernel_initializer.py
python3 su2_heat_kernel_initializer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_heat_kernel_initializer_theorem.tex
```

Expected: 14 tests pass.  Across all six computational stages, 68 tests pass.

## `SU(2)` nonlinear block geometry

From `08_su2_nonlinear_block_geometry`:

```bash
python3 -m unittest -v test_su2_nonlinear_block_geometry.py
python3 su2_nonlinear_block_geometry.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_nonlinear_block_geometry_theorem.tex
```

Expected: 19 tests pass.  Across all seven computational stages, 87 tests
pass.

## `SU(2)` ultraviolet overlap

From `09_su2_uv_overlap`:

```bash
python3 -m unittest -v test_su2_uv_overlap.py
python3 su2_uv_overlap.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_uv_overlap_theorem.tex
```

Expected: 17 tests pass.  Across all eight computational stages, 104 tests
pass.

## Frustrated-conditioning obstruction

From `10_frustrated_conditioning_obstruction`:

```bash
python3 -m unittest -v test_frustrated_conditioning.py
python3 frustrated_conditioning.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error frustrated_conditioning_theorem.tex
```

Expected: 17 tests pass.  Across all nine computational stages, 121 tests
pass.

## Good-collar coherence

From `11_good_collar_coherence`:

```bash
python3 -m unittest -v test_good_collar_coherence.py
python3 good_collar_coherence.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error good_collar_coherence_theorem.tex
```

Expected: 13 tests pass.  Across all ten computational stages, 134 tests
pass.

## Center-contour charging

From `12_center_contour_charging`:

```bash
python3 -m unittest -v test_center_contour_charging.py
python3 center_contour_charging.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error center_contour_charging_theorem.tex
```

Expected: 16 tests pass.  Across all eleven computational stages, 150 tests
pass.

## Dependent Gaussian connected events

From `13_dependent_gaussian_polymers`:

```bash
python3 -m unittest -v test_dependent_gaussian_polymers.py
python3 dependent_gaussian_polymers.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error dependent_gaussian_polymers_theorem.tex
```

Expected: 13 tests pass.  Across all twelve computational stages, 163 tests
pass.

## Nonlinear connected-event transfer

From `14_nonlinear_activity_transfer`:

```bash
python3 -m unittest -v test_nonlinear_activity_transfer.py
python3 nonlinear_activity_transfer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error nonlinear_activity_transfer_theorem.tex
```

Expected: 15 tests pass.  Across all thirteen computational stages, 178 tests
pass.

The last two theorems bound connected bad-event envelopes.  Their tests do not
certify a Mayer/Ursell activity expansion.  Stage 18 later supplies stochastic
domination as an alternative conversion under a stronger adaptive premise.

## Nonasymptotic good-collar conditional

From `15_nonasymptotic_good_collar`:

```bash
python3 -m unittest -v test_nonasymptotic_good_collar.py
python3 nonasymptotic_good_collar.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error nonasymptotic_good_collar_theorem.tex
```

Expected: 12 tests pass.  Across all fourteen computational stages, 190 tests
pass.

## Continuous collar charging

From `16_continuous_collar_charging`:

```bash
python3 -m unittest -v test_continuous_collar_charging.py
python3 continuous_collar_charging.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error continuous_collar_charging_theorem.tex
```

Expected: 13 tests pass.  Across all fifteen computational stages, 203 tests
pass.

## Chart density comparison

From `17_chart_density_comparison`:

```bash
python3 -m unittest -v test_chart_density_comparison.py
python3 chart_density_comparison.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error chart_density_comparison_theorem.tex
```

Expected: 13 tests pass.  Across all sixteen computational stages, 216 tests
pass.

## Adaptive stochastic domination

From `18_adaptive_stochastic_domination`:

```bash
python3 -m unittest -v test_adaptive_stochastic_domination.py
python3 adaptive_stochastic_domination.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error adaptive_stochastic_domination_theorem.tex
```

Expected: 15 tests pass.  Across all seventeen computational stages, 231
tests pass.

## State-weighted defect transfer

From `19_state_weighted_defect_transfer`:

```bash
python3 -m unittest -v test_state_weighted_defect_transfer.py
python3 state_weighted_defect_transfer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error state_weighted_defect_transfer_theorem.tex
```

Expected: 13 tests pass. Across all eighteen computational stages, 244 tests
pass.

## `SU(2)` boundary-state disintegration

From `20_su2_boundary_state_disintegration`:

```bash
python3 -m unittest -v test_su2_boundary_state_disintegration.py
python3 su2_boundary_state_disintegration.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_boundary_state_theorem.tex
```

Expected: 14 tests pass. Across all nineteen computational stages, 258 tests
pass.

## Curvature-local typical-set atlas

From `21_curvature_typical_set_atlas`:

```bash
python3 -m unittest -v test_curvature_typical_set_atlas.py
python3 curvature_typical_set_atlas.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error curvature_typical_set_theorem.tex
```

Expected: 13 tests pass. Across all twenty computational stages, 271 tests
pass.

## Sharp nonlinear overlap

From `22_sharp_nonlinear_overlap`:

```bash
python3 -m unittest -v test_sharp_nonlinear_overlap.py
python3 sharp_nonlinear_overlap.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error sharp_nonlinear_overlap_theorem.tex
```

Expected: 14 tests pass. Across all twenty-one computational stages, 285 tests
pass.

## Local-cylinder normalized comparison

From `23_local_cylinder_comparison`:

```bash
python3 -m unittest -v test_local_cylinder_comparison.py
python3 local_cylinder_comparison.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error local_cylinder_comparison_theorem.tex
```

Expected: 12 tests pass. Across all twenty-two computational stages, 297 tests
pass.

## Multichannel retained-state weights

From `24_multichannel_state_weights`:

```bash
python3 -m unittest -v test_multichannel_state_weights.py
python3 multichannel_state_weights.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error multichannel_state_weights_theorem.tex
```

Expected: 12 tests pass. Across all twenty-three computational stages, 309
tests pass.

## One-scale `K+R` composition

From `25_one_scale_kr_composition`:

```bash
python3 -m unittest -v test_one_scale_kr_composition.py
python3 one_scale_kr_composition.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error one_scale_kr_composition_theorem.tex
```

Expected: 12 tests pass. Across all twenty-four computational stages, 321
tests pass.

## Conditional partition-ratio frontier

From `26_partition_ratio_frontier`:

```bash
python3 -m unittest -v test_partition_ratio_frontier.py
python3 partition_ratio_frontier.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error partition_ratio_frontier_theorem.tex
```

Expected: 12 tests pass. Through Stage 26, the twenty-five computational
stages have 333 tests.

## Exact `SU(2)` Haar entropy

From `27_su2_haar_entropy`:

```bash
python3 -m unittest -v test_su2_haar_entropy.py
python3 su2_haar_entropy.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_haar_entropy_theorem.tex
```

Expected: 15 tests pass.

## Coherent partition optimizer

From `28_coherent_partition_optimizer`:

```bash
python3 -m unittest -v test_coherent_partition_optimizer.py
python3 coherent_partition_optimizer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error coherent_partition_optimizer_theorem.tex
```

Expected: 15 tests pass.

## Coherence--charge trade-off

From `29_coherence_charge_tradeoff`:

```bash
python3 -m unittest -v test_coherence_charge_tradeoff.py
python3 coherence_charge_tradeoff.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error coherence_charge_tradeoff_theorem.tex
```

Expected: 19 tests pass.

## Channelwise partition frontier

From `30_channelwise_partition_frontier`:

```bash
python3 -m unittest -v test_channelwise_partition_frontier.py
python3 channelwise_partition_frontier.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error channelwise_partition_frontier_theorem.tex
```

Expected: 15 tests pass. Across all twenty-nine computational stages, 397
tests pass.

## Exact Fréchet collar charge

From `31_frechet_collar_charge`:

```bash
python3 -m unittest -v test_frechet_collar_charge.py
python3 frechet_collar_charge.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error frechet_collar_charge_theorem.tex
```

Expected: 13 tests pass.

## Dispersion conditional optimizer

From `32_dispersion_conditional_optimizer`:

```bash
python3 -m unittest -v test_dispersion_conditional_optimizer.py
python3 dispersion_conditional_optimizer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error dispersion_conditional_optimizer_theorem.tex
```

Expected: 13 tests pass.

## Canonical plaquette witness

From `33_canonical_plaquette_witness`:

```bash
python3 -m unittest -v test_canonical_plaquette_witness.py
python3 canonical_plaquette_witness.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error canonical_plaquette_witness_theorem.tex
```

Expected: 13 tests pass.

## Entropy-complete plaquette activity

From `34_entropy_complete_plaquette_activity`:

```bash
python3 -m unittest -v test_entropy_complete_plaquette_activity.py
python3 entropy_complete_plaquette_activity.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error entropy_complete_plaquette_activity_theorem.tex
```

Expected: 12 tests pass.

## Linearized dispersion spectrum

From `35_linearized_dispersion_spectrum`:

```bash
python3 -m unittest -v test_linearized_dispersion_spectrum.py
python3 linearized_dispersion_spectrum.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error linearized_dispersion_spectrum_theorem.tex
```

Expected: 15 tests pass.

## Adaptive dispersion filtration

From `36_adaptive_dispersion_filtration`:

```bash
python3 -m unittest -v test_adaptive_dispersion_filtration.py
python3 adaptive_dispersion_filtration.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error adaptive_dispersion_filtration_theorem.tex
```

Expected: 14 tests pass.

## Partition repair congestion

From `37_partition_repair_congestion`:

```bash
python3 -m unittest -v test_partition_repair_congestion.py
python3 partition_repair_congestion.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error partition_repair_congestion_theorem.tex
```

Expected: 14 tests pass.

## Sector-aware numerator atlas

From `38_sector_aware_numerator_atlas`:

```bash
python3 -m unittest -v test_sector_aware_numerator_atlas.py
python3 sector_aware_numerator_atlas.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error sector_aware_numerator_atlas_theorem.tex
```

Expected: 13 tests pass.

## Periodic center-flux topology

From `39_periodic_center_flux_topology`:

```bash
python3 -m unittest -v test_periodic_center_flux_topology.py
python3 periodic_center_flux_topology.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error periodic_center_flux_topology_theorem.tex
```

Expected: 14 tests pass.

## Dispersion programme frontier

From `40_dispersion_program_frontier`:

```bash
python3 -m unittest -v test_dispersion_program_frontier.py
python3 dispersion_program_frontier.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error dispersion_program_frontier_theorem.tex
```

Expected: 15 tests pass. Across all thirty-nine computational stages, 533
tests pass through Stage 40.

## Nonlinear dispersion geometry

From `41_nonlinear_dispersion_geometry`:

```bash
python3 -m unittest -v test_nonlinear_dispersion_geometry.py
python3 nonlinear_dispersion_geometry.py
latexmk -pdf -interaction=nonstopmode -halt-on-error nonlinear_dispersion_geometry_theorem.tex
```

Expected: 13 tests pass.

## Dispersion-tail transfer

From `42_dispersion_tail_transfer`:

```bash
python3 -m unittest -v test_dispersion_tail_transfer.py
python3 dispersion_tail_transfer.py
latexmk -pdf -interaction=nonstopmode -halt-on-error dispersion_tail_transfer_theorem.tex
```

Expected: 14 tests pass.

## Centered star repair

From `43_centered_star_repair`:

```bash
python3 -m unittest -v test_centered_star_repair.py
python3 centered_star_repair.py
latexmk -pdf -interaction=nonstopmode -halt-on-error centered_star_repair_theorem.tex
```

Expected: 14 tests pass.

## Link-lift spillover

From `44_link_lift_spillover`:

```bash
python3 -m unittest -v test_link_lift_spillover.py
python3 link_lift_spillover.py
latexmk -pdf -interaction=nonstopmode -halt-on-error link_lift_spillover_theorem.tex
```

Expected: 15 tests pass.

## Coordinated-repair frontier

From `45_coordinated_repair_frontier`:

```bash
python3 -m unittest -v test_coordinated_repair_frontier.py
python3 coordinated_repair_frontier.py
latexmk -pdf -interaction=nonstopmode -halt-on-error coordinated_repair_frontier_theorem.tex
```

Expected: 14 tests pass.

## History-uniform dispersion comparison

From `46_history_uniform_dispersion_comparison`:

```bash
python3 -m unittest -v test_history_uniform_dispersion_comparison.py
python3 history_uniform_dispersion_comparison.py
latexmk -pdf -interaction=nonstopmode -halt-on-error history_uniform_dispersion_comparison_theorem.tex
```

Expected: 14 tests pass.

## Center-flux sector barriers

From `47_center_flux_sector_barriers`:

```bash
python3 -m unittest -v test_center_flux_sector_barriers.py
python3 center_flux_sector_barriers.py
latexmk -pdf -interaction=nonstopmode -halt-on-error center_flux_sector_barriers_theorem.tex
```

Expected: 15 tests pass.

## Integer topology carrier

From `48_integer_topology_carrier`:

```bash
python3 -m unittest -v test_integer_topology_carrier.py
python3 integer_topology_carrier.py
latexmk -pdf -interaction=nonstopmode -halt-on-error integer_topology_carrier_theorem.tex
```

Expected: 15 tests pass.

## Updated multichannel budget

From `49_updated_multichannel_budget`:

```bash
python3 -m unittest -v test_updated_multichannel_budget.py
python3 updated_multichannel_budget.py
latexmk -pdf -interaction=nonstopmode -halt-on-error updated_multichannel_budget_theorem.tex
```

Expected: 14 tests pass.

## Nonlinear-transfer frontier

From `50_nonlinear_transfer_frontier`:

```bash
python3 -m unittest -v test_nonlinear_transfer_frontier.py
python3 nonlinear_transfer_frontier.py
latexmk -pdf -interaction=nonstopmode -halt-on-error nonlinear_transfer_frontier_theorem.tex
```

Expected: 15 tests pass. Across all forty-nine computational stages, 676
tests pass.

## Run the full computational regression

From the package root:

```bash
for stage in 02_relational_rigidity_program \
             03_heat_kernel_basin_entry \
             04_fibered_block_rg \
             05_su2_quotient_fiber \
             06_one_step_effective_action \
             07_su2_heat_kernel_initializer \
             08_su2_nonlinear_block_geometry \
             09_su2_uv_overlap \
             10_frustrated_conditioning_obstruction \
             11_good_collar_coherence \
             12_center_contour_charging \
             13_dependent_gaussian_polymers \
             14_nonlinear_activity_transfer \
             15_nonasymptotic_good_collar \
             16_continuous_collar_charging \
             17_chart_density_comparison \
             18_adaptive_stochastic_domination \
             19_state_weighted_defect_transfer \
             20_su2_boundary_state_disintegration \
             21_curvature_typical_set_atlas \
             22_sharp_nonlinear_overlap \
             23_local_cylinder_comparison \
             24_multichannel_state_weights \
             25_one_scale_kr_composition \
             26_partition_ratio_frontier \
             27_su2_haar_entropy \
             28_coherent_partition_optimizer \
             29_coherence_charge_tradeoff \
             30_channelwise_partition_frontier \
             31_frechet_collar_charge \
             32_dispersion_conditional_optimizer \
             33_canonical_plaquette_witness \
             34_entropy_complete_plaquette_activity \
             35_linearized_dispersion_spectrum \
             36_adaptive_dispersion_filtration \
             37_partition_repair_congestion \
             38_sector_aware_numerator_atlas \
             39_periodic_center_flux_topology \
             40_dispersion_program_frontier \
             41_nonlinear_dispersion_geometry \
             42_dispersion_tail_transfer \
             43_centered_star_repair \
             44_link_lift_spillover \
             45_coordinated_repair_frontier \
             46_history_uniform_dispersion_comparison \
             47_center_flux_sector_barriers \
             48_integer_topology_carrier \
             49_updated_multichannel_budget \
             50_nonlinear_transfer_frontier; do
  python3 -m unittest discover -v "$stage"
done
```

Expected: all 676 tests pass.

## VS Code Codex skill bundle

From `11_vscode_codex_skill_bundle`:

```bash
python3 verify_bundle.py
python3 install_skills.py --scope repo --repo /path/to/a/clean/repository --dry-run
python3 install_skills.py --scope repo --repo /path/to/a/clean/repository
```

Expected: the validator reports 29 unique valid skills and the orchestrator
`ym-run-clay-program`; the installer copies all 29 skills to
`.agents/skills`, verifies their bytes, and treats a repeated installation as
29 unchanged skills.

### LaTeX/PDF automation smoke test

From `11_vscode_codex_skill_bundle`:

```bash
skill=.agents/skills/ym-build-latex-paper
work=$(mktemp -d)
python3 "$skill/scripts/scaffold_paper.py" "$work/paper" \
  --title "Verified publication workflow" --author "Anonymous"
python3 "$skill/scripts/lint_manuscript.py" \
  "$work/paper/main.tex" --strict-narrative
python3 "$skill/scripts/render_paper.py" \
  "$work/paper/main.tex" --strict
```

Expected: the scaffold is created without overwriting existing data; the lint
report has no errors or workflow warnings; `latexmk` produces a PDF; metadata,
text extraction, references, and citations validate; first/middle/last page
PNGs are created; and `build/build_report.json` reports `status: passed`.

## Publication portfolio

From `51_publication_portfolio`:

```bash
python3 validate_publication_plans.py
```

Expected: four independent plans, 153 unique todo IDs, 153 total todos, all
referenced package sources present, and all four drafting skills present in the
portable skill bundle.

### Paper 01 manuscript

From `51_publication_portfolio/paper_01_frustrated_conditioning`:

```bash
python3 supplement/verify_incidence.py \
  --output supplement/incidence_certificate.json
python3 -m unittest -v supplement/test_verify_incidence.py
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/lint_manuscript.py \
  main.tex --strict-narrative --json build/lint_report.json
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/render_paper.py \
  main.tex --strict
```

Expected: 5 exact incidence tests pass; strict lint has zero errors and zero
narrative warnings; the PDF has 21 pages, no unresolved citations or
references, no overfull boxes, and SHA-256
`a2f339a7bad9b02c5ec9c53973ac09006c530ffc7311effd39d3a10c4063812a`.
The first, middle, and last preview pages are recorded as visually clean.

### Paper 02 manuscript

From `51_publication_portfolio/paper_02_verified_finite_block`:

```bash
python3 supplement/verify_finite_block.py \
  --output supplement/finite_block_certificate.json
python3 supplement/verify_independent.py \
  --output supplement/independent_certificate.json
python3 -m unittest -v supplement/test_verify_finite_block.py
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/lint_manuscript.py \
  main.tex --strict-narrative --json build/lint_report.json
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/render_paper.py \
  main.tex --strict
```

Expected: 11 tests pass; the two independent exact verifiers agree; strict
lint has zero errors and zero narrative warnings; the PDF has 18 pages, no
unresolved citations or references, no overfull boxes, and SHA-256
`c3461649a17b891cfb1c024564017f38e624b6375459a4a8c2dda7f133075a09`.
The first, middle, and last preview pages are recorded as visually clean.

### Paper 03 manuscript

From `51_publication_portfolio/paper_03_representational_dynamics`:

```bash
python3 supplement/representation_certificate.py \
  --output supplement/representation_certificate.json
python3 -m unittest -v supplement/test_representation_certificate.py
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/lint_manuscript.py \
  main.tex --strict-narrative --json build/lint_report.json
mkdir -p build_reproduction
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory=build_reproduction main.tex
bibtex build_reproduction/main
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory=build_reproduction main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -output-directory=build_reproduction main.tex
```

Expected: 13 exact tests pass; the JSON certificate reports
`all_checks_pass: true`; strict lint has zero errors and zero warnings; and the
PDF has 27 pages with no unresolved references/citations or overfull boxes.
The packaged PDF SHA-256 is
`e32b2e3228399efd32d93533cfd501086322e8d7f20508cf20151a95c33580c4`.
Eight representative pages, including both diagrams and the two-page
Yang--Mills certificate table, are recorded as visually clean.

### Paper 04 manuscript

From `51_publication_portfolio/paper_04_heat_kernel_enclosures`:

```bash
python3 supplement/exact_enclosures.py
python3 supplement/verify_certificate.py
python3 -m unittest -v supplement.test_heat_kernel_enclosures
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/lint_manuscript.py \
  main.tex --strict-narrative --json build/lint_report.json
python3 ../../11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/scripts/render_paper.py \
  main.tex --strict
```

Expected: 17 tests pass; all ten independent certificate checks pass; the
18-cell character/image diagnostic has discrepancy below `2e-12`; strict lint
has zero errors and warnings; and the PDF has 13 pages, no unresolved
references/citations, and no overfull boxes. The packaged PDF SHA-256 is
`f5a255d4ec525bc2ac76534e3cdd2923c115c9d76e8cefaa743d827b1016f5cc`.
The first, middle, and final previews are visually clean.

### Paper 05 manuscript

From `51_publication_portfolio/paper_05_staple_dispersion`:

```bash
python3 supplement/exact_linear_algebra.py --verify
python3 -m unittest supplement.test_exact_linear_algebra -v
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Expected: 5 tests pass; rational projection normal equations and complete KKT
systems verify for all eight interior links; the Gaussian spectrum is
`0, 239/630 (x2), 33/70 (x3)`; the spillover spectrum is
`37/33 (x3), 391/239 (x2)`; and the PDF has 15 pages with resolved references,
zero LaTeX warnings, and no overfull or underfull boxes.  Seven representative
pages, including both exact matrices, are recorded as visually clean.

## H1 vacuum-weight and five-target downstream run

From each of `53_h1_vacuum_weight` through `58_basin_os_frontier`, run the
stage's Python module with its documented `--write` target, then run its
`test_*.py` file with `python3 -m unittest -v`.  Compile Stages 54--58 with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Expected: Stage 53 passes 15 tests and emits a seven-page PDF. Stages 54--58
pass `9, 10, 11, 11, 11` tests and each emit a two-page PDF. Their build logs
contain no unresolved references and no overfull or underfull boxes. The
machine-readable results and theorem graphs validate with
`python3 -m json.tool`.

## H1--H10 independent next-step execution

From the package root, run:

```bash
for d in 68_h1_same_measure_calibration \
  69_h2_tempered_equivalence \
  70_h3_exact_multistar \
  71_h4_integral_topology_carrier \
  72_h5_information_partition_ratio \
  73_h6_typed_square_defects \
  74_h7_normalized_atlas_gluing \
  75_h8_certified_refinement \
  76_h9_dense_core_spectral \
  77_h10_observable_recovery
do
  python3 -m unittest discover -s "$d" -p 'test_*.py' -v
done
```

Expected per-stage counts are `18, 25, 14, 13, 23, 24, 16, 18, 20, 23`,
for 194/194 passing tests.  Validate the audit, registry, dependency graphs,
and canonical results with `python3 -m json.tool`.  Passing tests certify only
the declared finite fixtures and guardrails; they do not certify a nonlinear
physical `SU(2)` kernel, a continuum construction, or a mass gap.

## Verify package integrity

From the package root:

```bash
sha256sum -c CHECKSUMS.sha256
```
