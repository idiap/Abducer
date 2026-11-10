# Yang--Mills Representational Dynamics Research Package

Version: 2026-07-20

This archive collects the complete output of a representation-aware research
programme on the Yang--Mills existence and mass-gap problem. It contains the
philosophical ontology, mathematical representation calculus, Clay-target
decomposition, successive restricted-model attacks, executable calibrations,
tests, and theorem-status ledgers.

The package contains seven compiled documents (62 pages), their LaTeX sources,
three machine-readable theorem dependency graphs, three numerical calibration
datasets, four computational modules, and 31 passing automated tests.

## Epistemic status

This package is a research programme and a restricted theorem suite. It does
not construct four-dimensional continuum Yang--Mills theory and does not prove
the Clay mass-gap problem.

The proved contributions include finite spectral lemmas, representation-error
composition, a heat-kernel translation obstruction, an exact two-plaquette
`U(1)` bridge, the Gaussian retained/fiber response split, an exact multiscale
covariance decomposition, an independent-defect cluster bound, and finite
product total-variation comparison. Continuum clustering and spectral transfer
results are explicitly conditional on hypotheses recorded in the ledgers.

## Recommended reading order

1. `01_conceptual_foundations/yang_mills_mass_gap_conceptual_difficulty.pdf`
   explains why the problem is hard across physical and mathematical
   representations.
2. `01_conceptual_foundations/phenomenon_preserving_representations_yang_mills.pdf`
   identifies the phenomena to preserve and the constructs that may be changed
   only with recovery theorems.
3. `01_conceptual_foundations/generative_relational_coherence_universe.pdf`
   develops the higher-level informational/relational ontology.
4. `01_conceptual_foundations/yang_mills_relational_rigidity_clay_program.pdf`
   returns that ontology to the exact Clay target.
5. `02_relational_rigidity_program/ym_relational_rigidity_program.pdf`
   formalizes representation packages, morphisms, rigidity witnesses, and the
   complete theorem dependency chain.
6. `03_heat_kernel_basin_entry/heat_kernel_basin_entry_attack.pdf`
   falsifies a naive worst-case TV basin and replaces it with a two-tier
   good-field/defect formulation.
7. `04_fibered_block_rg/fibered_block_rg_theorem.pdf`
   separates retained coarse information from eliminated fiber information and
   proves the exact covariance accounting theorem.

## Directory map

### `01_conceptual_foundations`

Four matched `.tex`/`.pdf` documents covering conceptual difficulty,
phenomenon-preserving representations, relational ontology, and the
representation-aware Clay programme.

### `02_relational_rigidity_program`

The main representation calculus, original detailed research plan, proof
ledger, theorem dependency graph, finite spectral implementation, and tests.

### `03_heat_kernel_basin_entry`

The first frontier attack: heat-kernel influence theorem, compact-group and
regulator calibrations, two-tier basin proposal, dependency graph, and tests.

### `04_fibered_block_rg`

The interacting-block refinement: retained/fiber distinction, two-plaquette
bridge implementation, covariance decomposition, defect and regulator bounds,
frontier ledger, and tests.

## Integrity and reproduction

- `MANIFEST.md` lists every included artifact.
- `CHECKSUMS.sha256` records SHA-256 checksums for all package files except the
  checksum file itself.
- `REPRODUCIBILITY.md` gives compilation and test commands.

