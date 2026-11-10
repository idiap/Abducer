<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hegelian Source Map For Abducer

## Disposition

The Hegelian Solver snapshot remains source evidence. Abducer adopts selected control concepts as native hypothesis-space artifacts and rejects a second runtime, copied agent tree, or proof-bypassing acceptance labels.

## Adopted Concepts

| Source idea | Abducer adaptation | Evidence |
| --- | --- | --- |
| Concept/crisis packet | `conceptual_pressure_packet` tied to dependency graph nodes | `external/hegelian-solver/refs`, `agentic/spec/conceptual_pressure_packet.schema.json` |
| Failure certificate | `abducer_failure_certificate` for blocked proof, bridge, source, or premise obligations | `agentic/spec/abducer_failure_certificate.schema.json` |
| Discovery signal | Positive structural pressure from repeated route shapes or bridge opportunity | `agentic/spec/abducer_discovery_signal.schema.json` |
| Mediation candidate | Creative route transformation over Abducer artifacts | `agentic/spec/abducer_mediation_candidate.schema.json` |
| Validation packet | Hard proof/source/non-collapse gates | `agentic/spec/abducer_validation_packet.schema.json` |
| Bounded reflection | `conceptual_refinement_trace` consumed by `work` and Looper gates | `artifacts/hegelian/conceptual_refinement_trace.json` |

## Rejected Material

- Standalone Hegelian CLI as Abducer entrypoint.
- Parallel `agents/` tree copied into `skills/`.
- Generic accept labels treated as proof.
- Creative terminology that cannot produce obligations, graph edges, or route dispositions.
