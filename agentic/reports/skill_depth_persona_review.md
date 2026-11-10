<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Skill Depth Persona Review

## Scope

Reviewed 61 repo-local skills under `skills/*/*/SKILL.md` through two lenses:

- **Mathematician:** definitions, theorem bodies, invariants, edge cases, proof obligations, and target-preserving transformations.
- **Epistemologist:** claim-to-evidence fit, hidden assumptions, uncertainty, falsification, disconfirming observations, and boundary conditions.

This review also checked whether skills push Codex toward real execution when needed: running bundled scripts, inspecting artifacts, and then doing generative interpretation instead of returning shallow deterministic placeholders.

## Strongest Supported Claims

- The skill hierarchy is no longer flat: skills are organized under control-plane, ingest, reasoning, discovery, evaluation, orchestration, reporting, and review themes.
- The generated skill projections and quality registry give every skill generic deterministic and generative boundary text.
- Several newer skills are deep and well shaped, especially the Hegelian/Abducer hypothesis-space skills:
  - `abducer-mediation-candidate-generator`
  - `abducer-conceptual-pressure-formalizer`
  - `abducer-failure-signal-cartographer`
  - `abducer-obligation-gatekeeper`
  - `abducer-refinement-route-ranker`
- The existing control plane can validate registries and workflow contracts, but it does not yet validate skill depth directly.

## Mathematician Findings

### M1. Output contracts are missing from many individual skills.

The audit found 27 skills without an explicit `Output Contract` section in the skill body. This matters because a mathematical skill must declare the shape of its mathematical product: theorem-shaped claim, proof obligation, route family, counterexample, bridge object, regime restriction, or epistemic status update.

Representative affected skills:

- `looper-target-dependency-cartographer`
- `looper-workflow-contract-governor`
- `kb-discovery-cycle`
- `kb-main-conjecture-grounder`
- `kb-prove-cycle`
- `bridge-object-equivalence-checker`
- `counterfactual-route-prober`
- `entailment-gap-auditor`
- `premise-completeness-prober`
- `regime-shift-auditor`
- `work`
- `expert-handoff`

### M2. Several evaluation skills do not explicitly require mathematical invariants.

Skills with names like bridge equivalence, entailment gap, premise completeness, counterfactual route probing, and regime-shift auditing should force invariants and edge cases into the output. Many currently imply the role but do not make the invariant discipline unavoidable.

Required invariant pattern:

- objects being compared,
- definitions/regimes preserved,
- assumptions added or removed,
- theorem body affected,
- edge case or countermodel searched,
- proof obligation emitted.

### M3. Script-backed skills risk becoming deterministic report emitters.

Many skills have useful scripts, but the skill body often says to run a script without requiring a second interpretive pass over the output. A mathematician would want:

1. run script,
2. inspect generated artifacts,
3. identify theorem-shaped consequences,
4. separate valid proof obligations from merely interesting graph signals,
5. emit next mathematical action.

Without this, a script can become an artifact factory rather than a proof-discovery skill.

## Epistemologist Findings

### E1. Epistemic status is under-specified in many skill bodies.

The audit found 34 skills without direct epistemic-status language such as uncertainty, falsification, disconfirmation, unsupported claims, or explicit unknowns. This is especially concerning for discovery and evaluation skills, because they often generate hypotheses that are plausible but not proven.

### E2. Registry-level quality text masks shallow skill bodies.

`agentic/registries/skill_quality_registry.yaml` currently gives every skill nearly identical high-level quality language. That is useful as a default, but it can hide whether the individual `SKILL.md` actually tells Codex how to behave deeply.

The validator currently checks projection shape, not whether each skill body contains the discipline it claims.

### E3. Falsification and demotion are not consistently first-class.

The best new hypothesis-space skills ask for disconfirming observations and quarantine. Older skills often ask for rankings or reports without forcing:

- what would falsify this route,
- what evidence would demote it,
- which boundary condition invalidates it,
- when to stop rather than continue.

## Codex-Exec Depth Finding

The skill pack should standardize an execution protocol:

```text
1. Identify required artifacts and missing context.
2. Run deterministic scripts or validators when available.
3. Inspect generated JSON/Markdown outputs.
4. Apply generative mathematical and epistemic review.
5. Emit typed outputs, uncertainties, and next actions.
```

This is different from both shallow deterministic behavior and free-form generative prose. The current skills apply this unevenly.

## High-Risk Skill Groups

1. **Control-plane skills**: need explicit output contracts and guardrails so they do not validate artifact presence as if it were mathematical progress.
2. **Evaluation skills**: need invariant, falsification, and demotion sections.
3. **Discovery/reporting skills**: need a script-plus-generative-interpretation protocol.
4. **Review skills**: need explicit persona output contracts and direct ties to TODO generation.
5. **Domain transfer to Yang-Mills**: target-control skills must handle physics/math target commitments, not only P vs NP-style route graphs.

## Gate Decision

Implementation can proceed, but the skill pack should not be considered fully deep or long-horizon safe until the TODOs in `agentic/todos/skill_depth_review_todos.yaml` are completed.
