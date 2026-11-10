---
name: framework-workflow-modeler
description: Extend extracted project workflow contracts into a typed, evidence-traceable workflow structure model for an AI framework paper. Use when Codex must preserve stages, skills, operators, artifacts, state stores, gates, validators, actors, handoffs, failure paths, persistence, and feedback loops without equating declared topology with runtime reachability.
---

# Framework Workflow Modeler

Use `$workflow-contract-extractor` and `$workflow-graph-modeler` as the canonical topology vocabulary; do not create a competing graph semantics.

1. Consume only the frozen evidence index and extracted workflow packet.
2. Model node types `workflow`, `stage`, `skill`, `operator`, `artifact`, `state_store`, `gate`, `validator`, and `actor`.
3. Model edge types `contains`, `invokes`, `consumes`, `produces`, `validates`, `gates`, `hands_off_to`, `persists_to`, and `feeds_back_to`.
4. Give every node and edge evidence IDs and an explicit posture where applicable.
5. Retain stop/failure paths and feedback loops.
6. Validate `WorkflowStructureModel` and bind it to the source-index digest.

Do not infer an executed path from documentation, registration, or graph connectivity. Refuse untraceable nodes and edges. Hand the model to abstraction and claim curation, not directly to writers.

## Recursive goals and workflow relationships

When this explanation is requested, read [the shared recursive-goals contract](../framework-core-mechanism-curator/references/recursive-goals-and-workflow-relations.md). Keep the existing closed WorkflowStructureModel unchanged. Put editorial goal dependencies and proposed cross-workflow relations in a separately labeled manual supplement, with source bindings and complete scope; do not pass new edge kinds off as native topology. This is a manual authoring extension, not a new fixed-runner schema or stage.
