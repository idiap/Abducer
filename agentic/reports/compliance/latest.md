<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Looper Compliance Report

- Target: `yang-mills-existence-and-mass-gap-target`
- Blocking acceptance gates: 3
- Dependency nodes: 97
- Open dependency frontier: 76
- Active TODO cards: 0

## Gate Evidence

- `target-packet-valid`: requires command:python agentic/scripts/validate_target_packets.py agentic/examples/targets/yang-mills-existence-and-mass-gap-target.json
- `dependency-graph-valid`: requires command:python agentic/scripts/validate_dependency_graph.py agentic/state/dependency_graphs/yang-mills-existence-and-mass-gap.json
- `target-relevance-ledger-valid`: requires command:python agentic/scripts/validate_target_relevance.py

## Frontier Health

- `accepted-local`: 21
- `blocked`: 3
- `bridge-obligation`: 33
- `proof-debt`: 39
- `tentative-local`: 1

## Compliance Decision

warn: control-plane evidence is present, but the mathematical target still has open proof/dependency frontier nodes.
