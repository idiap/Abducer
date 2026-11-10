---
name: framework-functional-modeler
description: Derive an evidence-backed functional capability model from a frozen repository evidence index. Use when Codex must explain what a framework does through inputs, outputs, state, preconditions, invariants, components, dependencies, validators, and limitations without reducing functionality to directory names or turning declarations into observed behavior.
---

# Framework Functional Modeler

Consume only a schema-valid `RepositoryEvidenceIndex`.

1. Group evidence into capabilities by externally meaningful behavior, not directory layout.
2. Record inputs, outputs, preconditions, invariants, components, dependencies, validators, and limitations for every capability.
3. Attach evidence IDs to every capability; require implementation or verification evidence for implementation claims.
4. Preserve conflicting authorities and missing evidence instead of choosing silently.
5. Validate `FunctionalCapabilityModel` and bind it to the source-index digest.

Do not write paper prose. Refuse capability statements with no source evidence. Hand the model to the abstraction and claim-curation stages.
