<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Granular conceptual workflow descriptions

Use this guide when a paper request asks how workflows reason at Prism level. It supplies the missing middle between a broad motif such as A–D–R–E and a dump of operation/type names.

For each workflow in the agreed scope, make the declared reasoning reconstructable:

- Explain the scientific question and the precise input/output boundary.
- For each occurrence, identify its local binding and reasoning operation; explain what input information it consumes, what conceptual transformation it makes, what its output adds or restricts, and what remains unestablished. Map concise aliases to exact source names in a sidecar.
- Show typed dependencies with generated wrappers, successful value projections and named record joins. A relation licenses a particular transition; explain the license, not merely its name. Retain the original claim/context when later calibration needs it.
- Distinguish sequence, parallel formation, joins and source-policy branches. Do not turn adjacent workflow names into direct composition without a matching boundary and adapter. Same-spelled types in different modules are not automatically identical.
- Explain one concrete constructed case through the defining transformations and its resulting inference. A reader should learn why this workflow differs from another even if the operation labels are removed.

An explicit `_` or projection gap is part of the description: state the required input and result of the missing transformation, what the following declared operation can do, and what the source does not supply. Explain a hypothetical desired use as hypothetical; do not invent an implemented algorithm to fill the hole. Granular source coverage can be complete while mechanism realization remains partial.

A compact typed display supports the mandatory seven-field step explanations in [the step contract](step-explanation-contract.md). Short explanations are acceptable only when every field and a continuous example transition remain reconstructable. Use longer diagrams only when branching or retained joins need them. Category/dependent notation supports these explanations; it does not replace them or imply native dependent enforcement.

Before delivery, reconcile all scoped workflow IDs, declared occurrences and relation uses against the source and the written sections. Record omitted or unresolved elements individually. A showcase workflow cannot stand in for the other scoped workflows. When actual paper revision is requested, verify these sections occur in the rebuilt manuscript, not just in isolated drafting previews. The assembler remains responsible for final integration; existing user authorization supplies the scope.
