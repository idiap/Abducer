<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Conceptual Creativity Quality Probes

These probes validate generative candidates produced by
`abducer-mediation-candidate-generator`.

## Quality Criteria

- Source grounding: every candidate cites pressure IDs, affected dependency nodes, and artifact paths.
- Mathematical specificity: the proposed transformation names the mathematical route object or obligation it changes.
- Creative operation fit: the operation is one of the declared conceptual creativity operations.
- Obligation completeness: preservation, target activation, non-collapse, barrier compatibility, source grounding, and proof-readiness are considered.
- Disconfirming observations: the candidate states how it could be demoted or falsified.
- Route usefulness: the candidate changes a disposition such as proof queue, discovery branch, revision loop, evidence task, quarantine, reject, or stop.

## Adversarial Cases

- Attractive mediator without source grounding must be quarantined.
- False analogy with missing mismatch inventory must not enter proof queue.
- Hidden assumption shift must become a representation-shift or revision item.
- Barrier-incompatible strengthening must be demoted unless barrier compatibility is explicit.
