<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Expert PDF trace grammar

An expert report uses the following reading grammar.

- **Identity:** trace, run, workflow, optional profile, version, target, packet digest, and lens.
- **Declared route:** each required, conditional, advisory, validator, or specialist role and its observed, justified-N/A, missing, failed, quarantined, or handed-off state.
- **Inference dossier:** stable event ID; step and skill; question; typed premises; operator; public warrant; conclusion; uncertainty; scope before and after; causal parents; independent integrity, epistemic, and disposition states.
- **Relations:** supporting, refuting, constraining, or background evidence; alternatives and their dispositions; falsifiers; obligations; artifacts and receipts; authority exercised and absent; prohibitions; gates; and handoffs.
- **Topology:** typed edges such as `precedes`, `contains`, `supports`, `refutes`, `constrains`, `produces`, `branches`, `joins`, `refines`, `validates`, `blocks`, and `hands-off`. A complete textual edge ledger accompanies any graphical summary.
- **Coverage:** source control, source semantics, evidence resolution, authority, HTML visibility, TeX inventory, and PDF visibility are reported separately.

Status is conveyed by words and symbols as well as color. Negative, minority, failed, quarantined, and open paths receive the same stable-ID visibility as successful paths. Empty lanes are printed explicitly rather than silently removed.

All packet-derived content is untrusted text. It is escaped centrally and may not enter the preamble, package list, command names, file arguments, URLs, or raw mathematics. Mathematical-looking input remains literal public text unless a future typed and separately validated trusted-math field is defined.

The grammar forbids scientific inference from layout, chronology, control events, integrity receipts, or coverage percentages. It also forbids status promotion, scope widening, novelty inflation, proof/release authority escalation, and finite-to-continuum promotion by the projection.

