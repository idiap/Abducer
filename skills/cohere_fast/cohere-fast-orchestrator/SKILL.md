---
name: cohere-fast-orchestrator
description: Execute the explicitly invoked, domain-bound cohere-fast lifecycle through Abducer-native child contracts and receipts.
---

# Cohere-fast orchestrator

Use only after validating a `cohere_fast_activation` receipt created from
`cohere-fast <domain> [subworkflow]`. Never infer activation from prose.

Consume a `DomainRunRequest`, execute the registered children in order, and
return a `CohereFastRunPacket`. Each child must return a typed packet; it may
not mutate parent state. Stop or quarantine according to the registry and do
not enter manuscript release without an accepted independent audit.

All artifacts and receipts belong under `cohere-fast/<domain>/<run>/`. Abducer
is the sole state authority. The imported Discover/TDR planner, CLI, and
SQLite state are reference material and must never become a control plane.

Workflow validity conveys no scientific correctness or proof authority.
