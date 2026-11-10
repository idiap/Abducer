# Abducer Repository PRISM Conversion

This tree is the deterministic conversion source for one Lunar package containing all
19 canonical Abducer reasoning workflows, all 359 skill trees, and all seven KB-backed
data sources. Each project keeps its source reasoning topology visible and provides a
separate `material_main.prism` whose occurrences execute as typed model-backed agents.

## Build and validate

Run the converter's `export_repository_prism.py` with repository root `.` and config
`prism-export.json`, passing the local Lunar checkout and `--verify-reproducible`.
Then run both the converter validator and `abducer-prism/validate_imported_prism_packages.py`
unchanged. Offline validity is necessary but not sufficient: import the archive through
Lunar, prepare its runtime, and validate one completed UI run per workflow.

## Interpreting results

A report-level final status of `passed` means the complete typed PRISM graph executed,
all declared occurrence transitions were recorded, and the result was rendered. It does
not mean a theorem was proved, an experiment ran, or a scientific claim was promoted.
The source-domain disposition inside `reasoning_result` may therefore be cautious or
negative while runtime verification correctly passes.

For example, `theorem_proof_delivery` may return a failure-certificate or quarantine
variant after all three reasoning steps complete. The run remains operationally valid;
the negative theorem disposition must remain visible and must not be rewritten as proof.
