<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Yang-Mills Representational Dynamics Integration TODOs

## Purpose

This document converts the two Yang-Mills source archives into a concrete
integration backlog for Abducer's discovery marathon workflow.

The goal is not to replace the existing target-neutral proof-depth stack. The
goal is to integrate a Yang-Mills-specific representational-dynamics overlay
that can drive better cycles on the Clay Yang-Mills existence and mass-gap
target while preserving conservative epistemic status, target scoping, and
publication-consolidation limits.

## Inputs

- Research package:
  `/Users/afreitas/Downloads/yang_mills_representational_dynamics_package_2026-07-20 (12).zip`
- VS Code/Codex skill bundle:
  `/Users/afreitas/Downloads/yang_mills_vscode_codex_skills_2026-07-20 (1).zip`

Both archives passed `unzip -tq` integrity checks on 2026-07-21.

The research package describes itself as a representation-aware Yang-Mills
research programme and restricted theorem suite. It contains seven compiled
documents, LaTeX sources, theorem dependency graphs, calibration datasets,
computational modules, and 31 automated tests. Its epistemic status is explicit:
it does not construct four-dimensional continuum Yang-Mills theory and does not
prove the Clay mass-gap problem.

The skill bundle exports 17 Yang-Mills workflow skills with orchestrator
`ym-run-clay-program` and five phases:

1. `target_and_language`
2. `regulators_and_scale_dynamics`
3. `constructive_frontier`
4. `continuum_and_spectrum`
5. `verification_and_governance`

## Integration Thesis

Abducer should treat the package as a target-scoped evidence and workflow
overlay for `yang-mills-existence-and-mass-gap-target`.

The incoming artifacts should be used to sharpen the YM workflow around:

- exact Clay target freezing;
- gauge-invariant observable completeness;
- representation packages, morphisms, and recovery certificates;
- noncircular relational-rigidity witnesses;
- regulator atlas design and gauge-covariant RG;
- infrared basin entry and basin-to-rigidity transfer;
- large-field and topological exceptional regimes;
- continuum Schwinger data, Osterwalder-Schrader reconstruction, and spectral
  transfer;
- restricted-model calibration, mechanized finite cores, and frontier audits.

The integration must not let a restricted finite or conditional result become a
global proof claim. It should instead make the restricted status visible and
useful: every result becomes a proof object with a claim level, hypotheses,
dependencies, falsifiers, and routing consequences.

## Non-Negotiable Guards

- **No Clay overclaim.** The package is a restricted theorem suite, not a Clay
  proof.
- **Target scoping.** YM artifacts and reports must live under
  `yang-mills-existence-and-mass-gap-target` paths or explicit YM integration
  paths. They must not overwrite P-vs-NP reports, latest pointers, or timeline
  outputs.
- **Repo-visible integration.** Preserve source provenance and expose adapted
  workflow surfaces inside the repository rather than relying only on global
  Codex skill installation.
- **No secret leakage.** Do not read or copy key material from
  `config/api_keys.json`; use existing secret-safe API-key validators when a
  marathon run is needed.
- **No epistemically lean skills.** The adapted skills must require conceptual
  depth, anti-definitionality audits, efficient representation requirements,
  explanatory power, unification power, falsifiability, and literature-boundary
  accounting.
- **Bounded publication consolidation.** A local subgoal can lock into a
  publication-consolidation window only after exploratory critical mass. The
  default limit remains four completion cycles and recursion depth one.

## Execution Plan

### Phase 0: Provenance and Integrity

Import the archives into a versioned repo-local evidence area without changing
their meaning. Record source paths, checksums, manifests, and verification
results. The imported package should remain auditable as external source
material.

### Phase 1: Evidence Index and Proof Objects

Create a machine-readable index that maps each document, theorem dependency
graph, calibration file, code module, test, and ledger to its workflow role.
Translate the restricted theorem outputs into target-scoped proof objects with
claim level, hypotheses, dependencies, and non-claims.

### Phase 2: Skill Adaptation

Preserve the original skill bundle intact, then adapt the 17 skills into
Abducer's canonical repo skill layout. Each adapted skill must use Abducer's
proof-depth contract and must be able to emit declarative learning events,
anti-definitionality audits, representation requirements, and frontier audit
status.

### Phase 3: Main Workflow Integration

Add a YM-specific dispatch overlay to the discovery marathon skill dispatch and
task registry. The overlay should activate only for
`yang-mills-existence-and-mass-gap-target`. It should compose with the existing
target-neutral phases instead of bypassing them.

### Phase 4: Validation and Smoke Cycle

Add validators that check the imported source index, adapted skill count,
target scoping, claim-level discipline, report paths, and restricted-model test
execution. Run an API-free smoke cycle before any Azure marathon.

### Phase 5: Publication or Demotion Loop

Use the imported results to select a bounded subgoal: relational rigidity,
heat-kernel basin entry, or fibered block RG. Either consolidate it into a
publication-grade artifact inside the cycle budget, or demote/quarantine it
with a precise blocked lemma and learning event.

## TODO Cards

The executable TODO cards are in:

```text
agentic/todos/ym_representational_dynamics_integration_todos.yaml
```

They are intentionally written as self-contained work packets with acceptance
criteria, blockers, evidence, and failure modes so the next implementation
cycle can execute them without depending on this chat context.
