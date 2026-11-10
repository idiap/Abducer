<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Orphan-Skill And Named-Workflow Integration Plan

Status: implemented  
Scope: `skills/`, `agentic/registries/`, `registry/tasks/`, `hooks/`, runtime code, and tests  
Non-goal: changing the behavior or cost of the current lightweight target-navigation workflows

## Outcome

Keep the existing lightweight workflows intact while giving specialized skills explicit, opt-in homes. A skill is not considered integrated merely because it is catalogued: its workflow, trigger, ordered position, input, output, gate, and hook authorization must be visible.

## What The Review Found

The repository has 218 local skills. All 218 are present in the global skill registry and taxonomy projection, but the integration surfaces disagree:

| Surface | Skills represented | Meaning |
|---|---:|---|
| Global skill registry | 218 | The package exists and passed registry/depth checks. |
| Visible task workflows | 94 | The skill is eligible under the current `PreSkillUse` policy. |
| Discovery dispatch matrix | 137 | The skill is required, conditional, or legacy-advisory in a discovery phase. |
| Both task and dispatch surfaces | 66 | The two declarations agree that the skill belongs somewhere. |
| Task or dispatch surface | 165 | The skill has at least one of the two main declarations. |
| Neither task nor dispatch | 53 | The skill needs a declared disposition, but is not necessarily unreachable. |

The 53 are not 53 runtime orphans. Incoming references from operator registries, Python orchestrators, skill compositions, and target-specific routes reduce the true no-incoming-edge set to 10:

| Disposition | Count | Skills | Action |
|---|---:|---|---|
| Catalog-only specialization | 3 | `kb-framework-state-formalizer`, `kb-main-conjecture-grounder`, `pvsnp-kb-parser` | Keep opt-in and declare the relevant named workflow. |
| Registered, but absent from a named top-level workflow | 4 | `results-elaboration-workflow-orchestrator`, `routea-open-point-orchestrator`, `routea-paper-attack-orchestrator`, `routea-second-wave-manuscript-integrator` | Add manuscript-result and Route-A workflow contracts. |
| Genuinely unintegrated relative to the skill's stated role | 3 | `theorem-body-normalizer`, `hub-bias-auditor`, `regime-shift-auditor` | Add them as mandatory or conditional quality gates. |

The strongest individual inconsistency is `theorem-body-normalizer`: its own contract describes it as a mandatory Phase 0 gate, but no incoming workflow edge invokes it.

There is also a documentation-sync defect. Six integrated skills are missing from `docs/reference/skills.md`: `theory-atlas-defect-compiler`, `central-formal-conceptual-routes`, `conceptual-frontier-deepening`, `pvsnp-negative-tactic-selector`, `formal-claim-producer`, and `literature-conditioned-invention-forger`.

## Why They Were Not Integrated

This is mainly an integration-model problem rather than a lack of skill implementation.

1. `promoted` is overloaded. In `skill_registry.yaml` it means catalogued and depth-checked, not reachable from a named workflow.
2. The registries evolved independently. Five workflow contracts, six visible task workflows, the discovery dispatch phases, and operator routes have no common workflow identifier or cross-registry foreign key.
3. The task manifests and dispatch matrix represent different ideas. Task manifests control hook eligibility; dispatch mixes required, conditional, and historical advisory skills.
4. The current validators are local. They confirm that referenced files or names exist, but do not prove complete coverage, workflow identity agreement, typed handoffs, or runtime reachability.
5. Some separation is deliberate. Results elaboration, Route A, deep conceptual exploration, and framework review are specialized or expensive and should not be inserted into every target-navigation cycle.
6. Several skills are prompt-level capabilities without an executable adapter. Only 9 of the 53 have their own `scripts/` directory. Declaring such skills in a composition is valid, but must not be reported as executable until an adapter, validator, and receipt exist.

## The Hook Defect

`hooks/scripts/pre_skill_use_policy.py` constructs one global set from every task manifest's `composed_skills`. This has two opposing effects:

- It blocks 124 of the 218 controlled skills, including skills reachable through the dispatch matrix or operator runtime but absent from task manifests.
- It can accept any of the 94 task-declared skills in the wrong workflow, phase, or target because the payload's workflow identity is not checked.

All task workflows currently point to the same `repo-hook-config` alias. The alias proves that a hook configuration exists; it does not bind a workflow to an event, condition, required input, decision scope, or output.

The deterministic hooks should remain lightweight and transparent. They must validate orchestration decisions, not make scientific decisions or silently run skills.

## Explicit Hook Contract

Every named workflow should bind the shared hook events using the following fields:

```yaml
hook_id: stable-policy-id
event: UserPromptSubmit | PreSkillUse | PostSkillUse | PreToolUse | Stop
phase: workflow phase or step number
condition: deterministic predicate
required_inputs: [typed payload fields or artifact references]
decision: recommend | accept | warn | block
emitted_artifact: optional trace or receipt type
```

The shared policies are:

| Event | Required behavior | Forbidden behavior |
|---|---|---|
| `UserPromptSubmit` | Recommend a workflow ID and explain the matched trigger. | Starting a workflow or choosing a theory. |
| `PreSkillUse` | Require workflow ID/version, target, step, membership, prerequisites, and conditional-activation evidence. | Authorizing from the global union of all workflows. |
| `PostSkillUse` | Validate the declared output type, expected artifact, epistemic status, and receipt. | Treating file existence alone as scientific acceptance. |
| `PreToolUse` | Enforce mutation, path, safety, and budget policy. | Performing hidden orchestration. |
| `Stop` | Evaluate the active workflow's exit artifacts and open obligations. | Requiring the same global Looper artifact tuple for every workflow. |

## Named Workflows

All new workflows are opt-in or typed-condition activated. None becomes part of the default target-navigation path.

### 1. `evidence_to_proof_route_onramp`

Activation: opt-in, bounded.  
Trigger: an external mathematical source, a missing/stale KB, or an explicit request to find an entrypoint or build a proof route.

Ordered skills and typed handoffs:

```text
SourceBundle
  -> latex-kb-ingest
  -> pvsnp-kb-parser                    [only for P-vs-NP LaTeX]
  -> theorem-body-normalizer
  -> kb-main-conjecture-grounder
  -> kb-proof-connector
  -> kb-hypothesis-evaluator            [when hypotheses exist]
  -> hub-bias-auditor
  -> kb-entrypoint-finder
  -> kb-entrypoint-pathfinder
  -> regime-shift-auditor               [when a path crosses regimes/models]
  -> counterexample-hunter
  -> expert-handoff
  -> ExpertRouteDossier
```

Exit gate: every statement has provenance and an assertion license; target implications are explicit; rankings survive anti-hub review; every promoted route has a falsifier or stop condition. The output goes to theorem proof delivery when theorem-shaped, otherwise to conceptual refinement.

### 2. `conceptual_frontier_deepening`

Activation: explicit opt-in, expensive.  
Trigger: a repeated blocker, representation failure, or explicit aggressive-conceptual-search request, plus a frozen target/theory/literature context and an approved budget.

```text
FrozenDiscoveryContext
  -> frontier-literature-assimilator
  -> literature-conditioned-invention-forger
  -> parallel-hypothesis-portfolio
  -> reflective-conceptual-discovery
  -> reflective-theory-synthesizer
  -> blind-conceptual-preference-adjudicator
  -> theory-atlas-defect-compiler       [only on category/HoTT pressure]
  -> central-formal-conceptual-routes
  -> bridge-object-equivalence-checker  [when multiple carriers compete]
  -> formal-claim-producer
  -> FormalClaimProducerOutputV2
```

Exit gate: exact ancestry, literature, and commit bindings; blind route-neutral adjudication; matched controls; no theory selection by experiments; only a ready-or-not-ready formal claim. Ready claims go to proof delivery. Non-dominated or not-ready candidates return to conceptual refinement with a learning delta.

### 3. `theorem_proof_delivery`

Activation: conditional, bounded.  
Trigger: a source-bound and target-bound queue item with an exact theorem-shaped statement.

```text
ProofQueueItem
  -> proof-delivery-workflow-orchestrator
  -> proof-obligation-formalizer
  -> lemma-chain-proof-builder
  -> proof-gap-countermodel-splitter     [when a lemma is blocked or false]
  -> pvsnp-inference-quality-controller [only for P-vs-NP]
  -> proof-quality-gatekeeper
  -> ProofGateDecision
```

Exit gate: exact definitions, quantifiers, assumptions, and non-claims; no circular lemma chain; every gap repaired, countermodeled, declared no-go, or quarantined. Accepted results may enter contribution cultivation. Failure certificates return to conceptual refinement.

### 4. `scientific_contribution_cultivation`

Activation: conditional, lightweight.  
Trigger: a result-atlas change, completed/handoff-ready subgoal, contribution checkpoint, or explicit paper-readiness review.

```text
ResultAtlasSlice
  -> result-atlas-maintainer
  -> contribution-oriented-subgoal-manager
  -> scientific-contribution-detector
  -> contribution-value-assessor
  -> main-problem-alignment-auditor
  -> completed-subgoal-enablement-auditor
  -> subgoal-enablement-handoff-packager [when enablement is non-empty]
  -> scientific-contribution-paper-handoff [when paper-ready]
  -> EnablementAudit | PaperArgumentHandoff
```

Exit gate: smallest honest claim; evidence for novelty, explanatory power, implications, generality, robustness, and validation burden; explicit mechanism relative to the main target. Support-only results stay support-only.

### 5. `manuscript_result_elaboration`

Activation: opt-in, bounded, and independent from discovery.  
Trigger: a draft with expansion markers, open modules, or an explicit result-elaboration request.

```text
PaperDraft
  -> results-elaboration-workflow-orchestrator
  -> results-context-interpreter
  -> results-extension-need-extractor | results-open-module-decomposer
  -> results-extension-strategy-planner
  -> results-critical-self-refiner
  -> results-theorem-scope-certifier
  -> results-finite-object-formalizer   [when a finite object is required]
  -> results-proof-packet-deriver       [for proof-class work]
  -> results-prior-art-disqualifier-auditor
  -> results-narrative-integrator
  -> results-expansion-validator
  -> results-paper-readiness-gatekeeper
  -> PaperReadinessDecision
```

Exit gate: every marker is covered; every TODO has a discharge or quarantine condition; finite, asymptotic, and continuum claims remain separated; prior-art boundaries and manuscript claims validate. This workflow must not invoke the discovery marathon.

Route-A is a profile of this workflow rather than another generic framework:

```text
routea-paper-attack-orchestrator
  -> routea-open-point-orchestrator
  -> selected module specialists
  -> routea-symbolic-cas-auditor        [when exact algebra is required]
  -> routea-paper-result-integrator
  -> routea-second-wave-manuscript-integrator
  -> generic result validation/readiness tail
```

The selector may use the collar, normalization, coefficient, margin, endpoint, factorization, redesign, and continuum-gap specialists. Every specialist must return the generic `ResultCandidatePacket`, so target-specific work reuses the common validation tail.

### 6. `deep_review_and_reorientation`

Activation: conditional, bounded.  
Trigger: repeated blockage, contradictory evidence, low explanatory power, a major release gate, or explicit deep review.

```text
RunEvidenceBundle
  -> kb-framework-state-formalizer
  -> review-reasoner personas in parallel
     including review-reasoner-radical-designer
  -> meta
  -> looper-workflow-contract-governor
  -> GovernedRepairQueue
```

Exit gate: severity-ranked and evidence-backed findings; explicit falsifiers and demotion reasons; deduplicated TODOs assigned to a workflow. Review has no proof, epistemic-upgrade, or release authority.

## Canonical Workflow Contract

The implementation should make one registry authoritative and generate task projections from it. Each workflow needs:

```yaml
id: stable_workflow_id
version: semver
activation: default | opt_in | conditional
owner_skill: registered-skill-id
target_scope: [target selectors]
trigger: {all_of: [], any_of: [], none_of: []}
input_artifact: {type: type-id, schema: path-or-registered-schema}
steps:
  - order: 10
    skill: registered-skill-id
    mode: required | conditional | advisory | validator_only
    when: deterministic predicate or null
    consumes: [artifact-type]
    produces: [artifact-type]
    on_failure: stop | quarantine | fallback:step-id
hooks: [explicit hook bindings]
exit_gate: {validator: path, consumes: type-id, allowed: []}
handoffs: [{when: predicate, workflow: workflow-id, artifact_type: type-id}]
prohibitions: []
cost_profile: lightweight | bounded | expensive
```

Every registered skill must also have one explicit integration disposition: `required`, `conditional`, `advisory`, `validator_only`, `standalone`, or `quarantined`, with a rationale. A declaration is not an execution claim: `executable` additionally requires an adapter, validator, and receipt contract.

## Implementation TODOs

### Slice A — Establish one source of workflow truth

- [x] Extend `agentic/registries/workflow_contracts.yaml`, or replace it with one versioned canonical workflow registry, using the contract above.
- [x] Preserve the existing lightweight workflow definitions and behavior unchanged.
- [x] Give task workflow names and workflow contracts the same stable IDs and enforce foreign keys.
- [x] Record one explicit disposition and rationale for all 218 skills.
- [x] Generate `registry/tasks/*/task_registry.json` projections from the canonical contracts instead of maintaining parallel composition lists by hand.

Acceptance: all 218 skills are conserved exactly once in the disposition report; existing default workflows remain semantically unchanged; no duplicate or unknown workflow ID exists.

### Slice B — Register the six workflows and Route-A profile

- [x] Add the six contracts above with triggers, typed steps, gates, handoffs, prohibitions, and cost profiles.
- [x] Add the Route-A profile under manuscript result elaboration.
- [x] Integrate `theorem-body-normalizer`, `hub-bias-auditor`, and `regime-shift-auditor` at the required positions.
- [x] Mark prompt-only skills as composed/advisory until a real executable adapter exists.
- [x] Add schemas for new artifact types before making their typed edges normative.

Acceptance: every one of the 53 task/dispatch-undeclared skills has a named-workflow disposition; all 10 no-incoming-edge skills gain an intentional workflow edge or explicit standalone rationale.

### Slice C — Make hook authorization workflow-local

- [x] Add workflow ID, version, target, phase/step, and conditional evidence to `PreSkillUse` payloads.
- [x] Replace the global-union authorization check with active-workflow membership and prerequisite checks.
- [x] Make `PostSkillUse` validate the declared output contract and emit a receipt.
- [x] Make `Stop` check the active workflow's exit artifacts and open obligations.
- [x] Keep `UserPromptSubmit` advisory and all hooks deterministic.

Acceptance: the correct skill/workflow pair passes; missing workflow identity, wrong workflow, wrong target, unknown skill, and an unactivated conditional skill fail closed. A skill cannot borrow authorization from another task manifest.

### Slice D — Repair cross-registry validation and reachability language

- [x] Validate global skill IDs, workflow IDs, hook IDs/events, gates, schemas, artifacts, validators, typed step order, and handoff compatibility across registries.
- [x] Validate every dispatch skill against the global registry without treating advisory membership as execution.
- [x] Replace the binary orphan label with the ladder `catalogued -> workflow_declared -> runtime_routed -> executable -> exercised -> consumed -> feedback_effective`.
- [x] Generate or set-check `docs/reference/skills.md` against the 218-skill registry.
- [x] Repair the six missing catalog entries.

Acceptance: no unexplained skill remains; advisory and conditional mentions never upgrade a skill to executable; executable requires a route and validator; exercised/consumed require receipt evidence.

### Slice E — Regression and negative testing

- [x] Add contract tests for every new named workflow.
- [x] Add one positive and several negative trigger fixtures per workflow.
- [x] Test typed handoff compatibility and output consumption.
- [x] Test that a normal target-navigation run invokes none of the new workflows.
- [x] Add mutation tests that remove or rename a skill, hook, workflow, schema, or gate and require validation to fail.
- [x] Run the existing task, dispatch, hook, operator, and workflow-contract suites unchanged.

Acceptance: existing lightweight workflows stay green; each new workflow activates only from its declared trigger; all new outputs are consumed or explicitly terminally archived.

## Release Rule

Do not call the integration complete when the registry files merely contain every skill name. Completion requires agreement among workflow declaration, workflow-local hook authorization, runtime route, typed output validation, and receipt-backed reachability at the level claimed for each skill.
