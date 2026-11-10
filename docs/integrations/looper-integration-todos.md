<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Looper Integration Analysis and TODOs

## Purpose

This document is the self-contained implementation backlog for integrating
Looper into Abducer.

The goal is not to replace Abducer's mathematical discovery skills. The goal is
to add a visible Looper-style control plane so that, for a chosen mathematical
target, Abducer can:

1. normalize the target into an explicit goal packet;
2. recursively discover and persist all dependency obligations;
3. navigate the proof-search space by typed workflow coordinates rather than
   broad skill-prose search;
4. apply skills only through declared workflow contracts and deterministic
   hook gates;
5. stop, revise, or promote work based on durable evidence rather than on
   narrative confidence.

## Inputs Reviewed

- Looper archive:
  `/Users/afreitas/Downloads/looper-repo-content-20260707-033817.zip`
- Abducer architecture:
  `docs/architecture/architecture.md`
- Abducer orchestration:
  `docs/architecture/orchestration.md`
- Abducer skill reference:
  `docs/reference/skills.md`
- Abducer deterministic orchestrator:
  `skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py`
- Abducer outer loop:
  `skills/orchestration/work/SKILL.md`
  and `skills/orchestration/work/scripts/run_work_cycle.py`
- Abducer persistent search-space utilities:
  `skills/common/search_space_tree.py`

## Integration Thesis

Abducer already has the domain engine: KB grounding, relational discovery,
hypothesis formation, pathway synthesis, proof queues, proof attempts,
InformalMathLib persistence, plausibility scoring, process graphs, and reasoning logs.

Looper supplies the missing meta-control layer:

- goal quality enrichment before a run starts;
- workflow-visible task registries;
- taxonomic skill/workflow navigation;
- explicit workflow contracts with required artifacts and validators;
- transparent deterministic hooks;
- dependency governance;
- compliance, drift, frame-adequacy, reachability, and promotion reports;
- TODO evidence discipline.

The integration should therefore make Looper an Abducer control plane over the
existing KB-centered engine. The visible unit should be the workflow. Skills,
hooks, scripts, and artifacts are supporting composition elements.

## Target Architecture

The target state introduces the following Abducer-local control directories:

```text
agentic/
  spec/                 Goal, target, dependency, hook, and workflow schemas.
  todos/                Structured TODO cards with evidence and blockers.
  registries/           Skill, hook, workflow, target, dependency, and gate registries.
  state/                Current target, dependency frontier, loop state, and graph state.
  traces/               Hook runs, skill applications, workflow executions.
  reports/              Compliance, drift, reachability, frame adequacy, releases.
  evals/                Hook fixtures, target-navigation fixtures, workflow fixtures.
  scripts/              Deterministic validators and report generators.
registry/
  tasks/<task-id>/      Workflow-visible task manifests and task-local drafts.
hooks/
  hooks.json            Transparent deterministic hook registry.
  scripts/              Small deterministic hook scripts only.
```

Abducer should keep its current `skills/` tree as the promoted mathematical
skill layer. Looper's `agents/skills/*/*` shape should not be copied blindly.
Instead, import only Looper meta-skills that add control-plane behavior, and
adapt them to Abducer naming, artifacts, and proof-search semantics.

## Control Model

### 1. Goal-Oriented Target Packet

Every controlled run starts from a `target_packet`:

- `target_id`
- `raw_goal`
- `kb_path`
- `main_claim_ids`
- `desired_output_type`
- `quality_criteria`
- `acceptance_gates`
- `known_constraints`
- `unknowns`
- `validation_targets`
- `evidence_paths`

This packet adapts Looper's goal enrichment packet to Abducer's mathematical
objects. It must be deterministic to validate, but it may be created by a
judgment-heavy skill.

### 2. Recursive Dependency Graph

The target packet expands into a recursive dependency graph:

- KB statement dependencies from `depends_on`;
- connector candidates and unresolved dependencies from
  `connection-analysis.json`;
- phyp support and target relations from `phyp/*.proof-hypotheses.yaml`;
- entrypoint/pathway obligations from `entrypoint-pathways.json`;
- bridge-plan obligations from `bridge-plan.json`;
- conjectured abstraction obligations from `concept-gap-abstractions.json`;
- proof-sketch obligations and abort conditions from `proof-sketches.json`;
- proof queue entries and proof attempts from `proof-queue.*` and
  `proof-attempts/`;
- InformalMathLib results and blocked memory from `InformalMathLib/<kb-ref>/`.

The graph must classify each dependency as one of:

- `grounded`
- `accepted-local`
- `tentative-local`
- `external-prior-art-needed`
- `missing-premise`
- `bridge-obligation`
- `route-lemma`
- `proof-debt`
- `blocked`
- `refuted`
- `stale`

The recursive expansion stops only when every open node is either resolved,
blocked with evidence, deferred with a TODO, or explicitly out of scope.

### 3. Workflow-Visible Registry

For each target, create:

```text
registry/tasks/<target-id>/task_registry.json
```

The manifest must put `visible_workflows` first. Each visible workflow must
declare:

- end-to-end function;
- key function;
- reasoning types;
- problem domain types;
- task context types;
- composed Abducer skills;
- deterministic hooks;
- workflow references;
- artifacts;
- validators;
- current gate status.

This prevents the integration from becoming a hidden script bundle.

### 4. Hook-Controlled Skill Application

Hooks must remain deterministic and transparent. They may warn, block, or log.
They must not perform hidden reasoning or hidden orchestration.

Abducer hook events should include:

- `UserPromptSubmit`: require target enrichment when the prompt asks for broad
  proof search, "fully solve", "systematically navigate", or "keep working".
- `PreSkillUse`: check that the skill is declared in the active workflow and
  that its prerequisites exist.
- `PostSkillUse`: check that the expected artifacts, logs, and dependency
  updates were produced.
- `PreToolUse`: block destructive commands and warn on protected control-plane
  edits without TODO or decision evidence.
- `Stop`: block stopping a controlled iteration unless current target,
  dependency frontier, compliance report, drift report, and next TODO evidence
  exist.

### 5. Skill Navigation

Skill selection should not start by reading every `SKILL.md`.

Add taxonomy projection cards for Abducer skills:

- reasoning type: grounding, relational discovery, abduction, deduction,
  induction, proof-sketching, critique, revision, reflection, visualization;
- problem domain: theorem discovery, functional analysis, complexity theory,
  gauge theory, proof engineering, prior-art grounding;
- workflow role: intake, connector, evaluator, planner, generator, critic,
  compiler, prover, governor, reporter;
- inputs and outputs;
- deterministic boundaries;
- generative boundaries;
- prerequisites;
- validators;
- failure modes.

The Looper-style navigator should reduce the candidate set through these
projection cards before any generative judgment is used.

## Implementation TODOs

Each TODO below should eventually become a structured card under
`agentic/todos/`. The Markdown form is intentionally complete enough to guide
the implementation before that machinery exists.

### LINT-001: Create the Abducer Looper Control Plane Skeleton

- Status: open
- Priority: critical
- Risk class: architecture
- Owner: integration/control-plane
- Use skills: `kb-orchestrator`, `work`, Looper `long-horizon-loop-runner`
- Required artifacts:
  - `agentic/spec/`
  - `agentic/todos/`
  - `agentic/registries/`
  - `agentic/state/`
  - `agentic/traces/`
  - `agentic/reports/`
  - `agentic/evals/`
  - `agentic/scripts/`
  - `registry/tasks/`
  - `hooks/scripts/`
- Acceptance criteria:
  - Empty directories have purposeful `.gitkeep` or seed files.
  - `README.md` and `docs/README.md` describe the control plane.
  - No Abducer mathematical skill is moved or renamed.
  - The skeleton validates with a first `agentic/scripts/agentic_check.py`.
- Failure modes to watch:
  - Copying Looper wholesale and obscuring Abducer's existing architecture.
  - Creating a second parallel skill tree that competes with `skills/`.

### LINT-002: Define Abducer Goal and Target Packet Schemas

- Status: open
- Priority: critical
- Risk class: validation
- Owner: target-schema
- Use skills: Looper `goal-quality-enricher`, `kb-orchestrator`
- Required artifacts:
  - `agentic/spec/target_packet_schema.json`
  - `agentic/spec/goal_enrichment_packet_schema.json`
  - `agentic/examples/targets/p-vs-np-target.json`
  - `agentic/scripts/validate_target_packets.py`
- Acceptance criteria:
  - A packet can identify KB path, main claims, desired output, constraints,
    validation targets, and evidence paths.
  - Validation rejects missing KB files, unknown statement IDs, empty acceptance
    gates, and evidence paths outside the repo.
  - The schema supports mathematical outputs: proof route, proof sketch,
    refutation, dependency map, expert handoff, and research-program update.
- Failure modes to watch:
  - Treating a raw problem title as a sufficient target.
  - Losing hard scope constraints during enrichment.

### LINT-003: Build a Recursive Dependency Extractor

- Status: open
- Priority: critical
- Risk class: epistemic
- Owner: dependency-closure
- Use skills: `kb-proof-connector`, `kb-entrypoint-pathfinder`,
  `kb-proof-sketcher`, `kb-discovery-cycle`, Looper `external-dependency-manager`
- Required artifacts:
  - `agentic/spec/dependency_graph_schema.json`
  - `agentic/scripts/build_target_dependency_graph.py`
  - `agentic/scripts/validate_dependency_graph.py`
  - `agentic/state/dependency_graphs/<target-id>.json`
  - `agentic/reports/dependency_closure/<target-id>.md`
- Acceptance criteria:
  - The extractor reads KB dependencies, connector unresolved dependencies,
    phyp links, pathways, bridge plans, conjecture obligations, proof sketches,
    proof queues, proof attempts, and InformalMathLib records when present.
  - Each node has type, status, source artifact, parent dependencies, blocker,
    and next action.
  - Cycles are detected and surfaced rather than recursively expanded forever.
  - Every open dependency has a next action or a blocking TODO.
- Failure modes to watch:
  - Dependency recursion becomes a graph dump without actionable frontier nodes.
  - Connector similarity is mistaken for proof dependency.

### LINT-004: Make Target Navigation the First Visible Workflow

- Status: open
- Priority: critical
- Risk class: architecture
- Owner: workflow-registry
- Use skills: Looper `taxonomic-skill-navigator`, `planning-todo-manager`,
  `long-horizon-loop-runner`
- Required artifacts:
  - `registry/tasks/target-navigation/task_registry.json`
  - `registry/taxonomy/workflow_taxonomy.json`
  - `agentic/scripts/validate_task_skill_registry.py`
  - `agentic/reports/workflow_hub/latest.md`
- Acceptance criteria:
  - The task manifest has `visible_workflows` as the first operational section.
  - The target-navigation workflow declares composed skills, hooks, artifacts,
    validators, reasoning types, problem domains, and task contexts.
  - The validator fails if a workflow names undeclared skills, hooks,
    workflows, artifacts, or validators.
- Failure modes to watch:
  - Skills become the visible unit instead of workflows.
  - Workflow names drift from executable artifacts.

### LINT-005: Project Existing Abducer Skills Into Taxonomy Coordinates

- Status: open
- Priority: high
- Risk class: maintainability
- Owner: skill-registry
- Use skills: Looper `skill-taxonomy-classifier`, `taxonomic-skill-navigator`,
  `skill-reuse-auditor`
- Required artifacts:
  - `agentic/registries/skill_registry.yaml`
  - `agentic/registries/skill_quality_registry.yaml`
  - `registry/skill_projections/abducer_skill_projections.json`
  - `agentic/scripts/generate_skill_taxonomy_projections.py`
  - `agentic/scripts/validate_skill_taxonomy_projections.py`
- Acceptance criteria:
  - Every promoted Abducer skill has input, output, workflow role, boundaries,
    prerequisites, validators, and failure modes.
  - Projection validation rejects unknown taxonomy IDs, duplicate names, and
    missing workflow roles.
  - Prompt-only skills are clearly distinguished from deterministic scripts.
- Failure modes to watch:
  - Projection cards merely restate `SKILL.md` prose.
  - All proof skills receive the same broad classification and cannot be
    usefully navigated.

### LINT-006: Define Controlled Skill-Application Logs

- Status: open
- Priority: high
- Risk class: observability
- Owner: runtime-tracing
- Use skills: Looper `abductive-diagnostician`, `evidence-flow-interpreter`
- Required artifacts:
  - `agentic/spec/skill_application_log_schema.json`
  - `agentic/scripts/log_skill_application.py`
  - `agentic/scripts/validate_skill_application_logs.py`
  - `agentic/traces/skill_applications/<run-id>.jsonl`
  - `agentic/reports/skill_application_logs/<run-id>.md`
- Acceptance criteria:
  - Each skill invocation records workflow ID, target ID, skill ID, inputs,
    expected artifacts, produced artifacts, gate decision, dependency changes,
    and failure notes.
  - Logs correlate with Abducer's `ABDUCER_RUN_ID` reasoning logs.
  - Validation fails on missing lifecycle events.
- Failure modes to watch:
  - Duplicating Abducer reasoning logs without adding control-plane meaning.
  - Capturing hidden chain-of-thought instead of auditable summaries.

### LINT-007: Implement Transparent Hook Scripts

- Status: open
- Priority: high
- Risk class: governance
- Owner: hooks
- Use skills: Looper `hook-policy-maintainer`
- Required artifacts:
  - `hooks/hooks.json`
  - `hooks/scripts/user_prompt_submit_intake.py`
  - `hooks/scripts/pre_skill_use_policy.py`
  - `hooks/scripts/post_skill_use_review.py`
  - `hooks/scripts/pre_tool_use_policy.py`
  - `hooks/scripts/stop_artifact_check.py`
  - `agentic/evals/hook_contract/*.json`
  - `agentic/scripts/run_hook_contract_tests.py`
- Acceptance criteria:
  - Hooks only emit `accept`, `warn`, or `block` decisions plus reasons.
  - Hook tests cover accepted, warning, and blocking fixtures.
  - Hook scripts reject hidden orchestration markers and do not run reasoning
    stages themselves.
  - `Stop` requires current target, dependency frontier, compliance report,
    drift report, and next TODO evidence.
- Failure modes to watch:
  - Hooks quietly become the real workflow runner.
  - Hooks block normal exploratory reads that should remain cheap.

### LINT-008: Add Workflow Contract and Gate Registries

- Status: open
- Priority: high
- Risk class: validation
- Owner: workflow-contracts
- Use skills: Looper `gate-decision-interpreter`, `phase-transition-interpreter`
- Required artifacts:
  - `agentic/registries/workflow_contracts.yaml`
  - `agentic/registries/gate_policy.yaml`
  - `agentic/scripts/validate_workflow_contracts.py`
  - `agentic/scripts/apply_gate_policy.py`
- Acceptance criteria:
  - Contracts declare owner skill, required artifacts, validators, hook events,
    gates, and handoff workflows.
  - Gate policy normalizes pass, warn, fail, skip, waived, block, quarantine,
    and promote decisions.
  - Abducer `pipeline`, `abductive-loop`, and `work` routes have contracts.
- Failure modes to watch:
  - Contracts validate file existence but not lifecycle consistency.
  - Waivers become a way to skip evidence.

### LINT-009: Integrate Looper Gates Into `run_orchestrator.py`

- Status: open
- Priority: high
- Risk class: reliability
- Owner: orchestrator
- Use skills: `kb-orchestrator`, Looper `long-horizon-loop-runner`
- Required artifacts:
  - updates to `skills/orchestration/kb-orchestrator/scripts/run_orchestrator.py`
  - `agentic/scripts/check_stage_prerequisites.py`
  - `agentic/scripts/check_stage_outputs.py`
  - tests for gate success, warning, and blocking cases
- Acceptance criteria:
  - Before each deterministic stage, the orchestrator can consult the active
    workflow contract and target dependency graph.
  - After each stage, produced artifacts are checked against contract outputs.
  - Failures create diagnostic evidence and TODOs instead of silent continuation.
  - Existing direct orchestrator use remains possible when no Looper target is
    active.
- Failure modes to watch:
  - Breaking current CLI behavior for existing tests and runbooks.
  - Making all stages require the full Looper stack before migration is done.

### LINT-010: Integrate Dependency Frontier Into `work` Loop Decisions

- Status: open
- Priority: high
- Risk class: epistemic
- Owner: work-loop
- Use skills: `work`, `kb-discovery-cycle`, `kb-prove-cycle`,
  Looper `phase-transition-interpreter`
- Required artifacts:
  - updates to `skills/orchestration/work/scripts/run_work_cycle.py`
  - `agentic/state/current_target.json`
  - `agentic/state/dependency_frontier.json`
  - `agentic/reports/dependency_frontier/latest.md`
  - tests in `tests/orchestration/test_work_cycle.py`
- Acceptance criteria:
  - The work loop chooses discovery, prove, revise, or stop using the dependency
    frontier, not only queue availability and plausibility.
  - Stale, blocked, refuted, and high-reward dependencies are routed
    differently.
  - Each cycle updates frontier status and logs why the next phase was chosen.
- Failure modes to watch:
  - The work loop repeatedly revisits the same unresolved dependency.
  - Proof queue priority overrides explicit target dependencies.

### LINT-011: Add Compliance, Drift, and Frame-Adequacy Reports

- Status: open
- Priority: medium
- Risk class: governance
- Owner: reporting
- Use skills: Looper `compliance-assessor`, `drift-monitor-auditor`,
  `frame-adequacy-gate`
- Required artifacts:
  - `agentic/scripts/run_compliance_report.py`
  - `agentic/scripts/run_drift_monitors.py`
  - `agentic/scripts/run_frame_adequacy_report.py`
  - `agentic/reports/compliance/latest.md`
  - `agentic/reports/drift/latest.md`
  - `agentic/reports/frame_adequacy/latest.md`
- Acceptance criteria:
  - Compliance is requirement-driven and counts missing evidence.
  - Drift monitors cover target drift, dependency drift, skill-contract drift,
    artifact drift, and stale InformalMathLib or proof-queue state.
  - Frame adequacy identifies missing mathematical vocabulary, proxy-eval risk,
    unresolved distinctions, and promotion blockers.
- Failure modes to watch:
  - Reports become reassuring dashboards without blocking force.
  - Drift checks only prove that files exist.

### LINT-012: Add Skill Reachability and Workflow Hub Reports

- Status: open
- Priority: medium
- Risk class: maintainability
- Owner: reachability
- Use skills: Looper `skill-reuse-auditor`, `spec-graph-compiler`
- Required artifacts:
  - `agentic/scripts/run_skill_reachability_audit.py`
  - `agentic/scripts/run_workflow_hub_report.py`
  - `agentic/reports/skill_reachability/latest.md`
  - `agentic/reports/workflow_hub/latest.md`
  - `agentic/state/workflow_graph.json`
- Acceptance criteria:
  - Every promoted skill is classified as workflow-owner, direct-route,
    hook-policy, report-generator, validator-only, or explicitly deferred.
  - Workflow graph contains typed edges among targets, workflows, skills, hooks,
    artifacts, validators, gates, and handoffs.
  - Orphan promoted skills become TODOs or are explicitly quarantined.
- Failure modes to watch:
  - Reachability accepts mere trigger fixtures as workflow integration.
  - Workflow graph is generated but not validated.

### LINT-013: Add TODO Evidence Discipline

- Status: open
- Priority: medium
- Risk class: governance
- Owner: todo-manager
- Use skills: Looper `planning-todo-manager`
- Required artifacts:
  - `agentic/todos/todo_schema.yaml`
  - `agentic/todos/looper_integration_todos.yaml`
  - `agentic/scripts/validate_todos.py`
  - migration of this Markdown backlog into structured TODO cards
- Acceptance criteria:
  - Every TODO has ID, type, phase, owner, priority, risk class, intent,
    required artifacts, acceptance criteria, blockers, evidence, review date,
    failure modes, and status.
  - Resolved TODOs must cite file or command evidence.
  - TODO validation fails on missing blockers or missing evidence.
- Failure modes to watch:
  - TODOs become a checklist detached from validators.
  - Resolutions are marked complete without durable artifacts.

### LINT-014: Add a First Vertical Slice on `p-vs-np`

- Status: open
- Priority: high
- Risk class: reliability
- Owner: vertical-slice
- Use skills: `kb-orchestrator`, `work`, Looper `long-horizon-loop-runner`
- Required artifacts:
  - `agentic/examples/targets/p-vs-np-target.json`
  - `registry/tasks/p-vs-np-target-navigation/task_registry.json`
  - `agentic/state/dependency_graphs/p-vs-np.json`
  - `agentic/reports/dependency_closure/p-vs-np.md`
  - `agentic/reports/releases/ITER-0001.md`
- Acceptance criteria:
  - The run starts from a target packet and produces a dependency graph.
  - The visible workflow manifest names all composed skills and hooks.
  - At least one stage is gated before and after execution.
  - The stop hook accepts only after current target, dependency frontier,
    compliance, drift, and next TODO evidence exist.
- Failure modes to watch:
  - The vertical slice validates scaffolding without using a real Abducer target.
  - The slice becomes a full proof attempt rather than a control-plane proof.

### LINT-015: Add Regression Tests for the Integrated Control Plane

- Status: open
- Priority: high
- Risk class: reliability
- Owner: tests
- Use skills: Looper `eval-generator`
- Required artifacts:
  - `tests/orchestration/test_looper_target_packets.py`
  - `tests/orchestration/test_looper_dependency_graph.py`
  - `tests/orchestration/test_looper_workflow_registry.py`
  - `tests/orchestration/test_looper_hooks.py`
  - `tests/orchestration/test_looper_orchestrator_gates.py`
- Acceptance criteria:
  - Tests cover valid and invalid target packets.
  - Tests cover dependency closure with cycles and unresolved blockers.
  - Tests cover workflow manifests with undeclared skills/hooks/artifacts.
  - Tests cover hook accept, warn, and block decisions.
  - Tests cover orchestrator gate behavior without requiring external services.
- Failure modes to watch:
  - Tests rely on the current large artifact tree and become brittle.
  - Tests check only happy paths.

### LINT-016: Add Documentation and Runbook Updates

- Status: open
- Priority: medium
- Risk class: maintainability
- Owner: docs
- Use skills: `kb-framework-state-formalizer`, Looper `release-promoter`
- Required artifacts:
  - updates to `README.md`
  - updates to `docs/README.md`
  - `docs/integrations/looper-control-plane.md`
  - `docs/operations/target-navigation-runbook.md`
  - `docs/architecture/data-contracts.md` additions for target/dependency/workflow packets
- Acceptance criteria:
  - Docs explain that workflows are the visible unit.
  - Docs distinguish Abducer mathematical skills from Looper control-plane
    skills and hooks.
  - Runbook shows target packet -> dependency graph -> workflow manifest ->
    gated orchestrator run -> reports -> next TODO.
- Failure modes to watch:
  - Documentation advertises full integration before validators exist.
  - Docs use Looper terms without mapping them to Abducer artifacts.

### LINT-017: Establish Migration Boundaries for Imported Looper Code

- Status: open
- Priority: medium
- Risk class: dependency
- Owner: import-curation
- Use skills: Looper `external-framework-reuse-gate`,
  `external-dependency-manager`
- Required artifacts:
  - `agentic/registries/external_framework_registry.yaml`
  - `agentic/registries/dependency_registry.yaml`
  - `agentic/reports/external_framework_reuse/latest.md`
  - `agentic/reports/import_diff/looper_archive.md`
- Acceptance criteria:
  - Every imported Looper file is labeled `reuse_as_is`, `adapt`, `quarantine`,
    or `reject`.
  - Standard-library-only validators remain the default unless a dependency card
    justifies an external package.
  - Archive/readme mismatches are recorded before promotion.
- Failure modes to watch:
  - Vendored Looper claims become authoritative without validation.
  - Importing demo-specific oncology artifacts into Abducer's theorem workflow.

### LINT-018: Add Release Promotion for Controlled Iterations

- Status: open
- Priority: medium
- Risk class: governance
- Owner: release
- Use skills: Looper `release-promoter`, `gate-decision-interpreter`
- Required artifacts:
  - `agentic/scripts/validate_promotion_gates.py`
  - `agentic/reports/releases/ITER-*.md`
  - `agentic/reports/releases/latest.md`
- Acceptance criteria:
  - A release report cites target, workflow, dependency status, validators,
    regression safety, drift review, rollback path, and open blockers.
  - Promotion is impossible if critical dependency nodes remain unknown without
    TODOs or waivers.
  - Release status is one of promote, quarantine, rollback, or escalate.
- Failure modes to watch:
  - Release reports summarize work without enforcing gates.
  - Open blockers are hidden in narrative sections.

## Suggested Build Order

1. Implement LINT-001, LINT-002, and LINT-013 first so there is a control-plane
   skeleton, target packet, and TODO validation discipline.
2. Implement LINT-003 and LINT-004 next so the core target-navigation workflow
   exists.
3. Implement LINT-005, LINT-006, LINT-007, and LINT-008 to make skill
   application controlled and inspectable.
4. Implement LINT-009 and LINT-010 to wire the control plane into the current
   orchestrator and work loop without breaking direct usage.
5. Implement LINT-011, LINT-012, and LINT-018 to create governance reports and
   release decisions.
6. Implement LINT-014 and LINT-015 as the proof that the integration works on a
   real Abducer target.
7. Implement LINT-016 and LINT-017 throughout the process, not only at the end,
   because documentation and import boundaries are part of the safety surface.

## First Acceptance Bar

The integration should not be called "fully integrated" until the following
command passes from the repository root:

```bash
python agentic/scripts/agentic_check.py
python -m pytest tests/orchestration/test_looper_target_packets.py \
  tests/orchestration/test_looper_dependency_graph.py \
  tests/orchestration/test_looper_workflow_registry.py \
  tests/orchestration/test_looper_hooks.py \
  tests/orchestration/test_looper_orchestrator_gates.py
```

The first meaningful demonstration should be:

```bash
python agentic/scripts/run_target_navigation.py \
  --target agentic/examples/targets/p-vs-np-target.json
```

Expected outputs:

- `agentic/state/current_target.json`
- `agentic/state/dependency_graphs/p-vs-np.json`
- `agentic/reports/dependency_closure/p-vs-np.md`
- `registry/tasks/p-vs-np-target-navigation/task_registry.json`
- `agentic/reports/compliance/latest.md`
- `agentic/reports/drift/latest.md`
- `agentic/reports/releases/ITER-0001.md`

At that point, Abducer has Looper's central behavior: target-oriented,
recursive, dependency-aware, workflow-visible, hook-controlled skill
application with durable evidence.
