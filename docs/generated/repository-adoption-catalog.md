<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Repository adoption catalog

Generated ownership navigation for maintainers; regenerate with
`python3 proj_skills/scripts/repository_adoption_catalog.py --write` and check with `--check`.
Existing registries retain lookup authority. Scoped IDs distinguish domain-private names;
they do not add public aliases or grant activation, execution, scientific, or promotion authority.
Instruction contracts point to source documents; nearby helpers are never inferred callables.
Excluded sources remain reference material. Environment/cache directories are explicitly pruned in the JSON view.

## Registered pilot operations

| Operation | Existing owner implementation | Invocation |
| --- | --- | --- |
| `validate-project-skills` | [proj_skills/scripts/validate_proj_skills.py](../../proj_skills/scripts/validate_proj_skills.py) | cli |
| `render-history` | [proj_skills/scripts/repository_adoption_views.py](../../proj_skills/scripts/repository_adoption_views.py) | cli |
| `verify-view` | [proj_skills/scripts/repository_adoption_views.py](../../proj_skills/scripts/repository_adoption_views.py) | cli |
| `release-probe` | [proj_skills/scripts/repository_adoption_views.py](../../proj_skills/scripts/repository_adoption_views.py) | cli |

## Canonical skill ownership

| Scoped identity | Source contract | Disposition | Implementation |
| --- | --- | --- | --- |
| `abducer-prism/skills:to-prism` | [to-prism](../../abducer-prism/skills/to-prism/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-baseline` | [to-prism-baseline](../../abducer-prism/skills/to-prism-baseline/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-derive-types` | [to-prism-derive-types](../../abducer-prism/skills/to-prism-derive-types/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-design-parallel-tests` | [to-prism-design-parallel-tests](../../abducer-prism/skills/to-prism-design-parallel-tests/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-document-workflows` | [to-prism-document-workflows](../../abducer-prism/skills/to-prism-document-workflows/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-map-reasoning` | [to-prism-map-reasoning](../../abducer-prism/skills/to-prism-map-reasoning/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-model-workflows` | [to-prism-model-workflows](../../abducer-prism/skills/to-prism-model-workflows/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-review-preservation` | [to-prism-review-preservation](../../abducer-prism/skills/to-prism-review-preservation/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-run-parallel-tests` | [to-prism-run-parallel-tests](../../abducer-prism/skills/to-prism-run-parallel-tests/SKILL.md) | canonical | instruction-only |
| `abducer-prism/skills:to-prism-update` | [to-prism-update](../../abducer-prism/skills/to-prism-update/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-agent-contract-author` | [prism-agent-contract-author](../../prism_me/prism-agent-contract-author/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-agentic-shape-forger` | [prism-agentic-shape-forger](../../prism_me/prism-agentic-shape-forger/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-ai-researcher-review` | [prism-ai-researcher-review](../../prism_me/prism-ai-researcher-review/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-dependency-cartographer` | [prism-dependency-cartographer](../../prism_me/prism-dependency-cartographer/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-epistemologist-review` | [prism-epistemologist-review](../../prism_me/prism-epistemologist-review/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-external-capability-extractor` | [prism-external-capability-extractor](../../prism_me/prism-external-capability-extractor/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-external-reference-scoper` | [prism-external-reference-scoper](../../prism_me/prism-external-reference-scoper/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-generative-validation-runner` | [prism-generative-validation-runner](../../prism_me/prism-generative-validation-runner/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-implementation-driver` | [prism-implementation-driver](../../prism_me/prism-implementation-driver/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-integration-handoff` | [prism-integration-handoff](../../prism_me/prism-integration-handoff/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-mathematician-review` | [prism-mathematician-review](../../prism_me/prism-mathematician-review/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-persona-review-orchestrator` | [prism-persona-review-orchestrator](../../prism_me/prism-persona-review-orchestrator/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-quality-criteria-elicitor` | [prism-quality-criteria-elicitor](../../prism_me/prism-quality-criteria-elicitor/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-reflective-refinement-loop` | [prism-reflective-refinement-loop](../../prism_me/prism-reflective-refinement-loop/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-repo-cartographer` | [prism-repo-cartographer](../../prism_me/prism-repo-cartographer/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-slice-planner` | [prism-slice-planner](../../prism_me/prism-slice-planner/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-software-engineer-review` | [prism-software-engineer-review](../../prism_me/prism-software-engineer-review/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-spec-intake` | [prism-spec-intake](../../prism_me/prism-spec-intake/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-spec-orchestrator` | [prism-spec-orchestrator](../../prism_me/prism-spec-orchestrator/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-spec-verification-critic` | [prism-spec-verification-critic](../../prism_me/prism-spec-verification-critic/SKILL.md) | canonical | instruction-only |
| `prism_me:prism-test-strategy-architect` | [prism-test-strategy-architect](../../prism_me/prism-test-strategy-architect/SKILL.md) | canonical | instruction-only |
| `proj_skills:evolution-figure-builder` | [evolution-figure-builder](../../proj_skills/evolution-figure-builder/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-abstraction-synthesizer` | [framework-abstraction-synthesizer](../../proj_skills/framework-abstraction-synthesizer/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-core-mechanism-curator` | [framework-core-mechanism-curator](../../proj_skills/framework-core-mechanism-curator/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-evidence-indexer` | [framework-evidence-indexer](../../proj_skills/framework-evidence-indexer/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-execution-evidence-assessor` | [framework-execution-evidence-assessor](../../proj_skills/framework-execution-evidence-assessor/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-functional-modeler` | [framework-functional-modeler](../../proj_skills/framework-functional-modeler/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-abstract-writer` | [framework-paper-abstract-writer](../../proj_skills/framework-paper-abstract-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-architecture-writer` | [framework-paper-architecture-writer](../../proj_skills/framework-paper-architecture-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-blueprint-author` | [framework-paper-blueprint-author](../../proj_skills/framework-paper-blueprint-author/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-claim-curator` | [framework-paper-claim-curator](../../proj_skills/framework-paper-claim-curator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-conclusion-writer` | [framework-paper-conclusion-writer](../../proj_skills/framework-paper-conclusion-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-consistency-adjudicator` | [framework-paper-consistency-adjudicator](../../proj_skills/framework-paper-consistency-adjudicator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-core-mechanism-writer` | [framework-paper-core-mechanism-writer](../../proj_skills/framework-paper-core-mechanism-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-dependent-type-writer` | [framework-paper-dependent-type-writer](../../proj_skills/framework-paper-dependent-type-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-evaluation-writer` | [framework-paper-evaluation-writer](../../proj_skills/framework-paper-evaluation-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-figure-planner` | [framework-paper-figure-planner](../../proj_skills/framework-paper-figure-planner/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-implementation-writer` | [framework-paper-implementation-writer](../../proj_skills/framework-paper-implementation-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-introduction-writer` | [framework-paper-introduction-writer](../../proj_skills/framework-paper-introduction-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-latex-assembler` | [framework-paper-latex-assembler](../../proj_skills/framework-paper-latex-assembler/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-limitations-writer` | [framework-paper-limitations-writer](../../proj_skills/framework-paper-limitations-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-method-writer` | [framework-paper-method-writer](../../proj_skills/framework-paper-method-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-orchestrator` | [framework-paper-orchestrator](../../proj_skills/framework-paper-orchestrator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-related-work-writer` | [framework-paper-related-work-writer](../../proj_skills/framework-paper-related-work-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-taxonomy-plotter` | [framework-paper-taxonomy-plotter](../../proj_skills/framework-paper-taxonomy-plotter/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-validator` | [framework-paper-validator](../../proj_skills/framework-paper-validator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:framework-paper-workflow-appendix-writer` | [framework-paper-workflow-appendix-writer](../../proj_skills/framework-paper-workflow-appendix-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-paper-workflow-example-writer` | [framework-paper-workflow-example-writer](../../proj_skills/framework-paper-workflow-example-writer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-prism-workflow-extractor` | [framework-prism-workflow-extractor](../../proj_skills/framework-prism-workflow-extractor/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-reasoning-taxonomy-modeler` | [framework-reasoning-taxonomy-modeler](../../proj_skills/framework-reasoning-taxonomy-modeler/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-workflow-category-modeler` | [framework-workflow-category-modeler](../../proj_skills/framework-workflow-category-modeler/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-workflow-dependent-type-modeler` | [framework-workflow-dependent-type-modeler](../../proj_skills/framework-workflow-dependent-type-modeler/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-workflow-example-designer` | [framework-workflow-example-designer](../../proj_skills/framework-workflow-example-designer/SKILL.md) | canonical | instruction-only |
| `proj_skills:framework-workflow-modeler` | [framework-workflow-modeler](../../proj_skills/framework-workflow-modeler/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:functionality-milestone-classifier` | [functionality-milestone-classifier](../../proj_skills/functionality-milestone-classifier/SKILL.md) | canonical | instruction-only |
| `proj_skills:git-history-evolution-miner` | [git-history-evolution-miner](../../proj_skills/git-history-evolution-miner/SKILL.md) | canonical | instruction-only |
| `proj_skills:project-evolution-html-assembler` | [project-evolution-html-assembler](../../proj_skills/project-evolution-html-assembler/SKILL.md) | canonical | instruction-only |
| `proj_skills:project-evolution-timeline-reporter` | [project-evolution-timeline-reporter](../../proj_skills/project-evolution-timeline-reporter/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:project-onboarding-path-verifier` | [project-onboarding-path-verifier](../../proj_skills/project-onboarding-path-verifier/SKILL.md) | canonical | instruction-only |
| `proj_skills:project-readme-concept-builder` | [project-readme-concept-builder](../../proj_skills/project-readme-concept-builder/SKILL.md) | canonical | instruction-only |
| `proj_skills:project-readme-orchestrator` | [project-readme-orchestrator](../../proj_skills/project-readme-orchestrator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:project-state-profiler` | [project-state-profiler](../../proj_skills/project-state-profiler/SKILL.md) | canonical | instruction-only |
| `proj_skills:project-workflow-graph-reporter` | [project-workflow-graph-reporter](../../proj_skills/project-workflow-graph-reporter/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:workflow-contract-extractor` | [workflow-contract-extractor](../../proj_skills/workflow-contract-extractor/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-graph-html-reporter` | [workflow-graph-html-reporter](../../proj_skills/workflow-graph-html-reporter/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-graph-modeler` | [workflow-graph-modeler](../../proj_skills/workflow-graph-modeler/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-health-audit-orchestrator` | [workflow-health-audit-orchestrator](../../proj_skills/workflow-health-audit-orchestrator/SKILL.md) | canonical | instruction-with-helpers |
| `proj_skills:workflow-health-html-reporter` | [workflow-health-html-reporter](../../proj_skills/workflow-health-html-reporter/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-leakage-auditor` | [workflow-leakage-auditor](../../proj_skills/workflow-leakage-auditor/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-mock-behavior-auditor` | [workflow-mock-behavior-auditor](../../proj_skills/workflow-mock-behavior-auditor/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-orphan-skill-auditor` | [workflow-orphan-skill-auditor](../../proj_skills/workflow-orphan-skill-auditor/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-prompt-control-auditor` | [workflow-prompt-control-auditor](../../proj_skills/workflow-prompt-control-auditor/SKILL.md) | canonical | instruction-only |
| `proj_skills:workflow-test-coverage-auditor` | [workflow-test-coverage-auditor](../../proj_skills/workflow-test-coverage-auditor/SKILL.md) | canonical | instruction-only |
| `skills:cohere-fast-orchestrator` | [cohere-fast-orchestrator](../../skills/cohere_fast/cohere-fast-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:looper-hook-policy-maintainer` | [looper-hook-policy-maintainer](../../skills/control-plane/looper-hook-policy-maintainer/SKILL.md) | canonical | instruction-only |
| `skills:looper-release-promoter` | [looper-release-promoter](../../skills/control-plane/looper-release-promoter/SKILL.md) | canonical | instruction-only |
| `skills:looper-target-dependency-cartographer` | [looper-target-dependency-cartographer](../../skills/control-plane/looper-target-dependency-cartographer/SKILL.md) | canonical | instruction-only |
| `skills:looper-target-goal-enricher` | [looper-target-goal-enricher](../../skills/control-plane/looper-target-goal-enricher/SKILL.md) | canonical | instruction-only |
| `skills:looper-workflow-contract-governor` | [looper-workflow-contract-governor](../../skills/control-plane/looper-workflow-contract-governor/SKILL.md) | canonical | instruction-only |
| `skills:meta` | [meta](../../skills/control-plane/meta/SKILL.md) | canonical | instruction-with-helpers |
| `skills:abducer-mediation-candidate-generator` | [abducer-mediation-candidate-generator](../../skills/discovery/abducer-mediation-candidate-generator/SKILL.md) | canonical | instruction-only |
| `skills:categorical-concept-forger` | [categorical-concept-forger](../../skills/discovery/categorical-concept-forger/SKILL.md) | canonical | instruction-with-helpers |
| `skills:hott-equivalence-coherence-forger` | [hott-equivalence-coherence-forger](../../skills/discovery/hott-equivalence-coherence-forger/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-coherence-evaluator` | [kb-coherence-evaluator](../../skills/discovery/kb-coherence-evaluator/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-concept-bridge-planner` | [kb-concept-bridge-planner](../../skills/discovery/kb-concept-bridge-planner/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-discovery-cycle` | [kb-discovery-cycle](../../skills/discovery/kb-discovery-cycle/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-entrypoint-finder` | [kb-entrypoint-finder](../../skills/discovery/kb-entrypoint-finder/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-entrypoint-pathfinder` | [kb-entrypoint-pathfinder](../../skills/discovery/kb-entrypoint-pathfinder/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-epistemic-hardness` | [kb-epistemic-hardness](../../skills/discovery/kb-epistemic-hardness/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-framework-state-formalizer` | [kb-framework-state-formalizer](../../skills/discovery/kb-framework-state-formalizer/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-gap-abstraction-conjecturer` | [kb-gap-abstraction-conjecturer](../../skills/discovery/kb-gap-abstraction-conjecturer/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-main-conjecture-grounder` | [kb-main-conjecture-grounder](../../skills/discovery/kb-main-conjecture-grounder/SKILL.md) | canonical | instruction-only |
| `skills:kb-novel-proof-strategist` | [kb-novel-proof-strategist](../../skills/discovery/kb-novel-proof-strategist/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-prior-art-pass` | [kb-prior-art-pass](../../skills/discovery/kb-prior-art-pass/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-promising-direction-assessor` | [kb-promising-direction-assessor](../../skills/discovery/kb-promising-direction-assessor/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-proof-connector` | [kb-proof-connector](../../skills/discovery/kb-proof-connector/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-proof-sketcher` | [kb-proof-sketcher](../../skills/discovery/kb-proof-sketcher/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-prove-cycle` | [kb-prove-cycle](../../skills/discovery/kb-prove-cycle/SKILL.md) | canonical | instruction-with-helpers |
| `skills:theory-atlas-defect-compiler` | [theory-atlas-defect-compiler](../../skills/discovery/theory-atlas-defect-compiler/SKILL.md) | canonical | instruction-only |
| `cohere_fast/ym:ym-audit-frontier` | [ym-audit-frontier](../../skills/domain_specific/ym/ym-audit-frontier/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-build-gauge-covariant-rg` | [ym-build-gauge-covariant-rg](../../skills/domain_specific/ym/ym-build-gauge-covariant-rg/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-build-latex-paper` | [ym-build-latex-paper](../../skills/domain_specific/ym/ym-build-latex-paper/SKILL.md) | domain-private | instruction-with-helpers |
| `cohere_fast/ym:ym-build-observable-core` | [ym-build-observable-core](../../skills/domain_specific/ym/ym-build-observable-core/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-build-proof-appendix` | [ym-build-proof-appendix](../../skills/domain_specific/ym/ym-build-proof-appendix/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-build-representation-calculus` | [ym-build-representation-calculus](../../skills/domain_specific/ym/ym-build-representation-calculus/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-calibrate-restricted-models` | [ym-calibrate-restricted-models](../../skills/domain_specific/ym/ym-calibrate-restricted-models/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-control-large-fields-and-topology` | [ym-control-large-fields-and-topology](../../skills/domain_specific/ym/ym-control-large-fields-and-topology/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-define-relational-rigidity` | [ym-define-relational-rigidity](../../skills/domain_specific/ym/ym-define-relational-rigidity/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-design-infrared-basin` | [ym-design-infrared-basin](../../skills/domain_specific/ym/ym-design-infrared-basin/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-design-regulator-atlas` | [ym-design-regulator-atlas](../../skills/domain_specific/ym/ym-design-regulator-atlas/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-develop-paper-proofs` | [ym-develop-paper-proofs](../../skills/domain_specific/ym/ym-develop-paper-proofs/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-draft-finite-block-certificate` | [ym-draft-finite-block-certificate](../../skills/domain_specific/ym/ym-draft-finite-block-certificate/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-draft-frustration-obstruction` | [ym-draft-frustration-obstruction](../../skills/domain_specific/ym/ym-draft-frustration-obstruction/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-draft-heat-kernel-enclosures` | [ym-draft-heat-kernel-enclosures](../../skills/domain_specific/ym/ym-draft-heat-kernel-enclosures/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-draft-representational-dynamics` | [ym-draft-representational-dynamics](../../skills/domain_specific/ym/ym-draft-representational-dynamics/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-draft-staple-dispersion` | [ym-draft-staple-dispersion](../../skills/domain_specific/ym/ym-draft-staple-dispersion/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-frame-paper-narrative` | [ym-frame-paper-narrative](../../skills/domain_specific/ym/ym-frame-paper-narrative/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-freeze-clay-target` | [ym-freeze-clay-target](../../skills/domain_specific/ym/ym-freeze-clay-target/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-ground-paper-literature` | [ym-ground-paper-literature](../../skills/domain_specific/ym/ym-ground-paper-literature/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-mechanize-proof-core` | [ym-mechanize-proof-core](../../skills/domain_specific/ym/ym-mechanize-proof-core/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-adaptive-block-domination` | [ym-prove-adaptive-block-domination](../../skills/domain_specific/ym/ym-prove-adaptive-block-domination/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-basin-entry` | [ym-prove-basin-entry](../../skills/domain_specific/ym/ym-prove-basin-entry/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-conditional-partition-ratio` | [ym-prove-conditional-partition-ratio](../../skills/domain_specific/ym/ym-prove-conditional-partition-ratio/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-continuum-coherence` | [ym-prove-continuum-coherence](../../skills/domain_specific/ym/ym-prove-continuum-coherence/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-rg-to-rigidity` | [ym-prove-rg-to-rigidity](../../skills/domain_specific/ym/ym-prove-rg-to-rigidity/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-rigidity-transfer` | [ym-prove-rigidity-transfer](../../skills/domain_specific/ym/ym-prove-rigidity-transfer/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-prove-state-weighted-defect-transfer` | [ym-prove-state-weighted-defect-transfer](../../skills/domain_specific/ym/ym-prove-state-weighted-defect-transfer/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-reconstruct-os-gap` | [ym-reconstruct-os-gap](../../skills/domain_specific/ym/ym-reconstruct-os-gap/SKILL.md) | domain-private | instruction-only |
| `cohere_fast/ym:ym-run-clay-program` | [ym-run-clay-program](../../skills/domain_specific/ym/ym-run-clay-program/SKILL.md) | domain-private | instruction-only |
| `skills:abducer-conceptual-pressure-formalizer` | [abducer-conceptual-pressure-formalizer](../../skills/evaluation/abducer-conceptual-pressure-formalizer/SKILL.md) | canonical | instruction-only |
| `skills:abducer-failure-signal-cartographer` | [abducer-failure-signal-cartographer](../../skills/evaluation/abducer-failure-signal-cartographer/SKILL.md) | canonical | instruction-only |
| `skills:abducer-obligation-gatekeeper` | [abducer-obligation-gatekeeper](../../skills/evaluation/abducer-obligation-gatekeeper/SKILL.md) | canonical | instruction-only |
| `skills:abstraction-fit-gap-auditor` | [abstraction-fit-gap-auditor](../../skills/evaluation/abstraction-fit-gap-auditor/SKILL.md) | canonical | instruction-only |
| `skills:blind-conceptual-preference-adjudicator` | [blind-conceptual-preference-adjudicator](../../skills/evaluation/blind-conceptual-preference-adjudicator/SKILL.md) | canonical | instruction-only |
| `skills:bridge-object-equivalence-checker` | [bridge-object-equivalence-checker](../../skills/evaluation/bridge-object-equivalence-checker/SKILL.md) | canonical | instruction-only |
| `skills:completed-subgoal-enablement-auditor` | [completed-subgoal-enablement-auditor](../../skills/evaluation/completed-subgoal-enablement-auditor/SKILL.md) | canonical | instruction-only |
| `skills:contradiction-route-auditor` | [contradiction-route-auditor](../../skills/evaluation/contradiction-route-auditor/SKILL.md) | canonical | instruction-only |
| `skills:contribution-value-assessor` | [contribution-value-assessor](../../skills/evaluation/contribution-value-assessor/SKILL.md) | canonical | instruction-only |
| `skills:counterexample-hunter` | [counterexample-hunter](../../skills/evaluation/counterexample-hunter/SKILL.md) | canonical | instruction-only |
| `skills:counterfactual-route-prober` | [counterfactual-route-prober](../../skills/evaluation/counterfactual-route-prober/SKILL.md) | canonical | instruction-only |
| `skills:dimensional-symmetry-constraint-checker` | [dimensional-symmetry-constraint-checker](../../skills/evaluation/dimensional-symmetry-constraint-checker/SKILL.md) | canonical | instruction-only |
| `skills:entailment-gap-auditor` | [entailment-gap-auditor](../../skills/evaluation/entailment-gap-auditor/SKILL.md) | canonical | instruction-only |
| `skills:epistemic-status-ledger` | [epistemic-status-ledger](../../skills/evaluation/epistemic-status-ledger/SKILL.md) | canonical | instruction-only |
| `skills:failed-hypothesis-anticipator` | [failed-hypothesis-anticipator](../../skills/evaluation/failed-hypothesis-anticipator/SKILL.md) | canonical | instruction-only |
| `skills:failure-archaeology-explainer` | [failure-archaeology-explainer](../../skills/evaluation/failure-archaeology-explainer/SKILL.md) | canonical | instruction-only |
| `skills:gedanken-need-assessor` | [gedanken-need-assessor](../../skills/evaluation/gedanken-need-assessor/SKILL.md) | canonical | instruction-only |
| `skills:gedanken-transfer-guard` | [gedanken-transfer-guard](../../skills/evaluation/gedanken-transfer-guard/SKILL.md) | canonical | instruction-only |
| `skills:hub-bias-auditor` | [hub-bias-auditor](../../skills/evaluation/hub-bias-auditor/SKILL.md) | canonical | instruction-only |
| `skills:kb-discovery-breakthrough-profiler` | [kb-discovery-breakthrough-profiler](../../skills/evaluation/kb-discovery-breakthrough-profiler/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-discovery-governor` | [kb-discovery-governor](../../skills/evaluation/kb-discovery-governor/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-end-to-end-proof-critic` | [kb-end-to-end-proof-critic](../../skills/evaluation/kb-end-to-end-proof-critic/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-hypothesis-evaluator` | [kb-hypothesis-evaluator](../../skills/evaluation/kb-hypothesis-evaluator/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-hypothesis-refutation-loop` | [kb-hypothesis-refutation-loop](../../skills/evaluation/kb-hypothesis-refutation-loop/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-revision-loop` | [kb-revision-loop](../../skills/evaluation/kb-revision-loop/SKILL.md) | canonical | instruction-with-helpers |
| `skills:limit-convergence-behavior-auditor` | [limit-convergence-behavior-auditor](../../skills/evaluation/limit-convergence-behavior-auditor/SKILL.md) | canonical | instruction-only |
| `skills:literature-gap-relevance-auditor` | [literature-gap-relevance-auditor](../../skills/evaluation/literature-gap-relevance-auditor/SKILL.md) | canonical | instruction-only |
| `skills:main-problem-alignment-auditor` | [main-problem-alignment-auditor](../../skills/evaluation/main-problem-alignment-auditor/SKILL.md) | canonical | instruction-only |
| `skills:mathematical-concept-gap-revisitor` | [mathematical-concept-gap-revisitor](../../skills/evaluation/mathematical-concept-gap-revisitor/SKILL.md) | canonical | instruction-only |
| `skills:paper-contribution-readiness-judge` | [paper-contribution-readiness-judge](../../skills/evaluation/paper-contribution-readiness-judge/SKILL.md) | canonical | instruction-only |
| `skills:physical-relevance-impact-auditor` | [physical-relevance-impact-auditor](../../skills/evaluation/physical-relevance-impact-auditor/SKILL.md) | canonical | instruction-only |
| `skills:premise-completeness-prober` | [premise-completeness-prober](../../skills/evaluation/premise-completeness-prober/SKILL.md) | canonical | instruction-only |
| `skills:progression-payoff-judge` | [progression-payoff-judge](../../skills/evaluation/progression-payoff-judge/SKILL.md) | canonical | instruction-only |
| `skills:proof-conceptual-quality-heuristic-rater` | [proof-conceptual-quality-heuristic-rater](../../skills/evaluation/proof-conceptual-quality-heuristic-rater/SKILL.md) | canonical | instruction-only |
| `skills:proof-depth-pressure-formalizer` | [proof-depth-pressure-formalizer](../../skills/evaluation/proof-depth-pressure-formalizer/SKILL.md) | canonical | instruction-only |
| `skills:proof-depth-release-gate` | [proof-depth-release-gate](../../skills/evaluation/proof-depth-release-gate/SKILL.md) | canonical | instruction-only |
| `skills:proof-exploration-critical-mass-assessor` | [proof-exploration-critical-mass-assessor](../../skills/evaluation/proof-exploration-critical-mass-assessor/SKILL.md) | canonical | instruction-only |
| `skills:proof-inference-learning-extractor` | [proof-inference-learning-extractor](../../skills/evaluation/proof-inference-learning-extractor/SKILL.md) | canonical | instruction-only |
| `skills:proof-learning-ledger-maintainer` | [proof-learning-ledger-maintainer](../../skills/evaluation/proof-learning-ledger-maintainer/SKILL.md) | canonical | instruction-only |
| `skills:proof-nontriviality-auditor` | [proof-nontriviality-auditor](../../skills/evaluation/proof-nontriviality-auditor/SKILL.md) | canonical | instruction-only |
| `skills:proof-same-domain-transfer-certifier` | [proof-same-domain-transfer-certifier](../../skills/evaluation/proof-same-domain-transfer-certifier/SKILL.md) | canonical | instruction-only |
| `skills:proof-transfer-substance-auditor` | [proof-transfer-substance-auditor](../../skills/evaluation/proof-transfer-substance-auditor/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-barrier-specificity-reviewer` | [pvsnp-barrier-specificity-reviewer](../../skills/evaluation/pvsnp-barrier-specificity-reviewer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-conceptual-pressure-localizer` | [pvsnp-conceptual-pressure-localizer](../../skills/evaluation/pvsnp-conceptual-pressure-localizer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-meta-complexity-carrier-reviewer` | [pvsnp-meta-complexity-carrier-reviewer](../../skills/evaluation/pvsnp-meta-complexity-carrier-reviewer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-proof-complexity-transfer-reviewer` | [pvsnp-proof-complexity-transfer-reviewer](../../skills/evaluation/pvsnp-proof-complexity-transfer-reviewer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-quantifier-uniformity-reviewer` | [pvsnp-quantifier-uniformity-reviewer](../../skills/evaluation/pvsnp-quantifier-uniformity-reviewer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-reduction-consistency-reviewer` | [pvsnp-reduction-consistency-reviewer](../../skills/evaluation/pvsnp-reduction-consistency-reviewer/SKILL.md) | canonical | instruction-only |
| `skills:qualitative-physics-falsifier` | [qualitative-physics-falsifier](../../skills/evaluation/qualitative-physics-falsifier/SKILL.md) | canonical | instruction-only |
| `skills:regime-shift-auditor` | [regime-shift-auditor](../../skills/evaluation/regime-shift-auditor/SKILL.md) | canonical | instruction-only |
| `skills:scientific-contribution-detector` | [scientific-contribution-detector](../../skills/evaluation/scientific-contribution-detector/SKILL.md) | canonical | instruction-only |
| `skills:visual-analogy-preservation-auditor` | [visual-analogy-preservation-auditor](../../skills/evaluation/visual-analogy-preservation-auditor/SKILL.md) | canonical | instruction-only |
| `skills:visual-theorem-conceptualizer` | [visual-theorem-conceptualizer](../../skills/evaluation/visual-theorem-conceptualizer/SKILL.md) | canonical | instruction-only |
| `skills:evidence-acquisition-planner` | [evidence-acquisition-planner](../../skills/ingest/evidence-acquisition-planner/SKILL.md) | canonical | instruction-only |
| `skills:latex-kb-ingest` | [latex-kb-ingest](../../skills/ingest/latex-kb-ingest/SKILL.md) | canonical | instruction-with-helpers |
| `skills:prior-art-importer` | [prior-art-importer](../../skills/ingest/prior-art-importer/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-kb-parser` | [pvsnp-kb-parser](../../skills/ingest/pvsnp-kb-parser/SKILL.md) | canonical | instruction-with-helpers |
| `skills:target-literature-source-curator` | [target-literature-source-curator](../../skills/ingest/target-literature-source-curator/SKILL.md) | canonical | instruction-only |
| `skills:theorem-body-normalizer` | [theorem-body-normalizer](../../skills/ingest/theorem-body-normalizer/SKILL.md) | canonical | instruction-only |
| `skills:abducer-refinement-route-ranker` | [abducer-refinement-route-ranker](../../skills/orchestration/abducer-refinement-route-ranker/SKILL.md) | canonical | instruction-only |
| `skills:central-formal-conceptual-routes` | [central-formal-conceptual-routes](../../skills/orchestration/central-formal-conceptual-routes/SKILL.md) | canonical | instruction-only |
| `skills:conceptual-frontier-deepening` | [conceptual-frontier-deepening](../../skills/orchestration/conceptual-frontier-deepening/SKILL.md) | canonical | instruction-only |
| `skills:contribution-oriented-subgoal-manager` | [contribution-oriented-subgoal-manager](../../skills/orchestration/contribution-oriented-subgoal-manager/SKILL.md) | canonical | instruction-only |
| `skills:gedanken-followup-planner` | [gedanken-followup-planner](../../skills/orchestration/gedanken-followup-planner/SKILL.md) | canonical | instruction-only |
| `skills:kb-orchestrator` | [kb-orchestrator](../../skills/orchestration/kb-orchestrator/SKILL.md) | canonical | instruction-with-helpers |
| `skills:long-horizon-route-portfolio-manager` | [long-horizon-route-portfolio-manager](../../skills/orchestration/long-horizon-route-portfolio-manager/SKILL.md) | canonical | instruction-only |
| `skills:next-experiment-queue-ranker` | [next-experiment-queue-ranker](../../skills/orchestration/next-experiment-queue-ranker/SKILL.md) | canonical | instruction-only |
| `skills:orch` | [orch](../../skills/orchestration/orch/SKILL.md) | canonical | instruction-with-helpers |
| `skills:parallel-hypothesis-portfolio` | [parallel-hypothesis-portfolio](../../skills/orchestration/parallel-hypothesis-portfolio/SKILL.md) | canonical | instruction-only |
| `skills:proof-hard-gate-selector` | [proof-hard-gate-selector](../../skills/orchestration/proof-hard-gate-selector/SKILL.md) | canonical | instruction-only |
| `skills:proof-strategy-lockin-orchestrator` | [proof-strategy-lockin-orchestrator](../../skills/orchestration/proof-strategy-lockin-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-inference-quality-controller` | [pvsnp-inference-quality-controller](../../skills/orchestration/pvsnp-inference-quality-controller/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-negative-tactic-selector` | [pvsnp-negative-tactic-selector](../../skills/orchestration/pvsnp-negative-tactic-selector/SKILL.md) | canonical | instruction-only |
| `skills:reflective-conceptual-discovery` | [reflective-conceptual-discovery](../../skills/orchestration/reflective-conceptual-discovery/SKILL.md) | canonical | instruction-only |
| `skills:result-atlas-maintainer` | [result-atlas-maintainer](../../skills/orchestration/result-atlas-maintainer/SKILL.md) | canonical | instruction-only |
| `skills:route` | [route](../../skills/orchestration/route/SKILL.md) | canonical | instruction-with-helpers |
| `skills:show-reasoning` | [show-reasoning](../../skills/orchestration/show-reasoning/SKILL.md) | canonical | instruction-with-helpers |
| `skills:work` | [work](../../skills/orchestration/work/SKILL.md) | canonical | instruction-with-helpers |
| `skills:lemma-chain-proof-builder` | [lemma-chain-proof-builder](../../skills/proof_delivery/lemma-chain-proof-builder/SKILL.md) | canonical | instruction-only |
| `skills:proof-delivery-workflow-orchestrator` | [proof-delivery-workflow-orchestrator](../../skills/proof_delivery/proof-delivery-workflow-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:proof-gap-countermodel-splitter` | [proof-gap-countermodel-splitter](../../skills/proof_delivery/proof-gap-countermodel-splitter/SKILL.md) | canonical | instruction-only |
| `skills:proof-obligation-formalizer` | [proof-obligation-formalizer](../../skills/proof_delivery/proof-obligation-formalizer/SKILL.md) | canonical | instruction-only |
| `skills:proof-quality-gatekeeper` | [proof-quality-gatekeeper](../../skills/proof_delivery/proof-quality-gatekeeper/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-forcedrows-proof-workflow` | [pvsnp-forcedrows-proof-workflow](../../skills/proof_delivery/pvsnp-forcedrows-proof-workflow/SKILL.md) | canonical | instruction-only |
| `skills:dynamic-symbolic-simulation-experimenter` | [dynamic-symbolic-simulation-experimenter](../../skills/reasoning/dynamic-symbolic-simulation-experimenter/SKILL.md) | canonical | instruction-only |
| `skills:efficient-representation-requirements-elicitor` | [efficient-representation-requirements-elicitor](../../skills/reasoning/efficient-representation-requirements-elicitor/SKILL.md) | canonical | instruction-only |
| `skills:formal-claim-producer` | [formal-claim-producer](../../skills/reasoning/formal-claim-producer/SKILL.md) | canonical | instruction-only |
| `skills:frontier-literature-assimilator` | [frontier-literature-assimilator](../../skills/reasoning/frontier-literature-assimilator/SKILL.md) | canonical | instruction-only |
| `skills:gedanken-counterfactual-variant-builder` | [gedanken-counterfactual-variant-builder](../../skills/reasoning/gedanken-counterfactual-variant-builder/SKILL.md) | canonical | instruction-only |
| `skills:gedanken-situation-designer` | [gedanken-situation-designer](../../skills/reasoning/gedanken-situation-designer/SKILL.md) | canonical | instruction-only |
| `skills:high-risk-hypothesis-forger` | [high-risk-hypothesis-forger](../../skills/reasoning/high-risk-hypothesis-forger/SKILL.md) | canonical | instruction-only |
| `skills:kb-abduce` | [kb-abduce](../../skills/reasoning/kb-abduce/SKILL.md) | canonical | instruction-only |
| `skills:kb-contradiction-strategist` | [kb-contradiction-strategist](../../skills/reasoning/kb-contradiction-strategist/SKILL.md) | canonical | instruction-only |
| `skills:kb-deduce` | [kb-deduce](../../skills/reasoning/kb-deduce/SKILL.md) | canonical | instruction-only |
| `skills:kb-explain` | [kb-explain](../../skills/reasoning/kb-explain/SKILL.md) | canonical | instruction-only |
| `skills:kb-induce` | [kb-induce](../../skills/reasoning/kb-induce/SKILL.md) | canonical | instruction-only |
| `skills:literature-conditioned-invention-forger` | [literature-conditioned-invention-forger](../../skills/reasoning/literature-conditioned-invention-forger/SKILL.md) | canonical | instruction-only |
| `skills:monotonicity-sensitivity-prober` | [monotonicity-sensitivity-prober](../../skills/reasoning/monotonicity-sensitivity-prober/SKILL.md) | canonical | instruction-only |
| `skills:physics-regime-map-builder` | [physics-regime-map-builder](../../skills/reasoning/physics-regime-map-builder/SKILL.md) | canonical | instruction-only |
| `skills:proof-bridge-object-forger` | [proof-bridge-object-forger](../../skills/reasoning/proof-bridge-object-forger/SKILL.md) | canonical | instruction-only |
| `skills:proof-creative-variant-prober` | [proof-creative-variant-prober](../../skills/reasoning/proof-creative-variant-prober/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-gedanken-complexity-lab` | [pvsnp-gedanken-complexity-lab](../../skills/reasoning/pvsnp-gedanken-complexity-lab/SKILL.md) | canonical | instruction-with-helpers |
| `skills:pvsnp-impossibility-theorem-forger` | [pvsnp-impossibility-theorem-forger](../../skills/reasoning/pvsnp-impossibility-theorem-forger/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-pressure-bridge-forger` | [pvsnp-pressure-bridge-forger](../../skills/reasoning/pvsnp-pressure-bridge-forger/SKILL.md) | canonical | instruction-with-helpers |
| `skills:pvsnp-proof-derivation-builder` | [pvsnp-proof-derivation-builder](../../skills/reasoning/pvsnp-proof-derivation-builder/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-qualitative-complexity-reasoner` | [pvsnp-qualitative-complexity-reasoner](../../skills/reasoning/pvsnp-qualitative-complexity-reasoner/SKILL.md) | canonical | instruction-only |
| `skills:pvsnp-symbolic-complexity-auditor` | [pvsnp-symbolic-complexity-auditor](../../skills/reasoning/pvsnp-symbolic-complexity-auditor/SKILL.md) | canonical | instruction-with-helpers |
| `skills:qualitative-toy-model-builder` | [qualitative-toy-model-builder](../../skills/reasoning/qualitative-toy-model-builder/SKILL.md) | canonical | instruction-only |
| `skills:qualitative-variable-isolator` | [qualitative-variable-isolator](../../skills/reasoning/qualitative-variable-isolator/SKILL.md) | canonical | instruction-only |
| `skills:reflective-theory-synthesizer` | [reflective-theory-synthesizer](../../skills/reasoning/reflective-theory-synthesizer/SKILL.md) | canonical | instruction-only |
| `skills:scale-asymptotic-reasoner` | [scale-asymptotic-reasoner](../../skills/reasoning/scale-asymptotic-reasoner/SKILL.md) | canonical | instruction-only |
| `skills:endpoint-worked-calculation-packager` | [endpoint-worked-calculation-packager](../../skills/reporting/endpoint-worked-calculation-packager/SKILL.md) | canonical | instruction-only |
| `skills:expert-handoff` | [expert-handoff](../../skills/reporting/expert-handoff/SKILL.md) | canonical | instruction-only |
| `skills:finite-theorem-section-packager` | [finite-theorem-section-packager](../../skills/reporting/finite-theorem-section-packager/SKILL.md) | canonical | instruction-only |
| `skills:kb-expert-paper-generator` | [kb-expert-paper-generator](../../skills/reporting/kb-expert-paper-generator/SKILL.md) | canonical | instruction-with-helpers |
| `skills:kb-macro-proof-paper-writer` | [kb-macro-proof-paper-writer](../../skills/reporting/kb-macro-proof-paper-writer/SKILL.md) | canonical | instruction-with-helpers |
| `skills:prior-art-positioning-packager` | [prior-art-positioning-packager](../../skills/reporting/prior-art-positioning-packager/SKILL.md) | canonical | instruction-only |
| `skills:scientific-contribution-paper-handoff` | [scientific-contribution-paper-handoff](../../skills/reporting/scientific-contribution-paper-handoff/SKILL.md) | canonical | instruction-only |
| `skills:subgoal-enablement-handoff-packager` | [subgoal-enablement-handoff-packager](../../skills/reporting/subgoal-enablement-handoff-packager/SKILL.md) | canonical | instruction-only |
| `skills:target-literature-evolution-narrator` | [target-literature-evolution-narrator](../../skills/reporting/target-literature-evolution-narrator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-claim-boundary-auditor` | [timeline-claim-boundary-auditor](../../skills/reporting/timeline-claim-boundary-auditor/SKILL.md) | canonical | instruction-only |
| `skills:timeline-contribution-explainer` | [timeline-contribution-explainer](../../skills/reporting/timeline-contribution-explainer/SKILL.md) | canonical | instruction-only |
| `skills:timeline-contribution-stater` | [timeline-contribution-stater](../../skills/reporting/timeline-contribution-stater/SKILL.md) | canonical | instruction-only |
| `skills:timeline-cycle-latex-translator` | [timeline-cycle-latex-translator](../../skills/reporting/timeline-cycle-latex-translator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-definition-assumption-elicitor` | [timeline-definition-assumption-elicitor](../../skills/reporting/timeline-definition-assumption-elicitor/SKILL.md) | canonical | instruction-only |
| `skills:timeline-failed-route-interpreter` | [timeline-failed-route-interpreter](../../skills/reporting/timeline-failed-route-interpreter/SKILL.md) | canonical | instruction-only |
| `skills:timeline-formal-physics-deriver` | [timeline-formal-physics-deriver](../../skills/reporting/timeline-formal-physics-deriver/SKILL.md) | canonical | instruction-only |
| `skills:timeline-narrative-coherence-guard` | [timeline-narrative-coherence-guard](../../skills/reporting/timeline-narrative-coherence-guard/SKILL.md) | canonical | instruction-only |
| `skills:timeline-organizing-diagram-builder` | [timeline-organizing-diagram-builder](../../skills/reporting/timeline-organizing-diagram-builder/SKILL.md) | canonical | instruction-only |
| `skills:timeline-paper-argument-architect` | [timeline-paper-argument-architect](../../skills/reporting/timeline-paper-argument-architect/SKILL.md) | canonical | instruction-only |
| `skills:timeline-paper-cross-section-reconciler` | [timeline-paper-cross-section-reconciler](../../skills/reporting/timeline-paper-cross-section-reconciler/SKILL.md) | canonical | instruction-only |
| `skills:timeline-paper-section-synthesizer` | [timeline-paper-section-synthesizer](../../skills/reporting/timeline-paper-section-synthesizer/SKILL.md) | canonical | instruction-only |
| `skills:timeline-paper-workflow-orchestrator` | [timeline-paper-workflow-orchestrator](../../skills/reporting/timeline-paper-workflow-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-problem-literature-latex-translator` | [timeline-problem-literature-latex-translator](../../skills/reporting/timeline-problem-literature-latex-translator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-problem-space-narrator` | [timeline-problem-space-narrator](../../skills/reporting/timeline-problem-space-narrator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-reference-manager` | [timeline-reference-manager](../../skills/reporting/timeline-reference-manager/SKILL.md) | canonical | instruction-only |
| `skills:timeline-report-evidence-ingestor` | [timeline-report-evidence-ingestor](../../skills/reporting/timeline-report-evidence-ingestor/SKILL.md) | canonical | instruction-only |
| `skills:timeline-report-latex-composer` | [timeline-report-latex-composer](../../skills/reporting/timeline-report-latex-composer/SKILL.md) | canonical | instruction-only |
| `skills:timeline-story-latex-translator` | [timeline-story-latex-translator](../../skills/reporting/timeline-story-latex-translator/SKILL.md) | canonical | instruction-only |
| `skills:timeline-summary-latex-translator` | [timeline-summary-latex-translator](../../skills/reporting/timeline-summary-latex-translator/SKILL.md) | canonical | instruction-only |
| `skills:results-context-interpreter` | [results-context-interpreter](../../skills/results_ellaboration/results-context-interpreter/SKILL.md) | canonical | instruction-only |
| `skills:results-critical-self-refiner` | [results-critical-self-refiner](../../skills/results_ellaboration/results-critical-self-refiner/SKILL.md) | canonical | instruction-only |
| `skills:results-elaboration-workflow-orchestrator` | [results-elaboration-workflow-orchestrator](../../skills/results_ellaboration/results-elaboration-workflow-orchestrator/SKILL.md) | canonical | instruction-with-helpers |
| `skills:results-expansion-validator` | [results-expansion-validator](../../skills/results_ellaboration/results-expansion-validator/SKILL.md) | canonical | instruction-only |
| `skills:results-extension-need-extractor` | [results-extension-need-extractor](../../skills/results_ellaboration/results-extension-need-extractor/SKILL.md) | canonical | instruction-only |
| `skills:results-extension-strategy-planner` | [results-extension-strategy-planner](../../skills/results_ellaboration/results-extension-strategy-planner/SKILL.md) | canonical | instruction-only |
| `skills:results-finite-object-formalizer` | [results-finite-object-formalizer](../../skills/results_ellaboration/results-finite-object-formalizer/SKILL.md) | canonical | instruction-only |
| `skills:results-narrative-integrator` | [results-narrative-integrator](../../skills/results_ellaboration/results-narrative-integrator/SKILL.md) | canonical | instruction-only |
| `skills:results-open-module-decomposer` | [results-open-module-decomposer](../../skills/results_ellaboration/results-open-module-decomposer/SKILL.md) | canonical | instruction-only |
| `skills:results-paper-readiness-gatekeeper` | [results-paper-readiness-gatekeeper](../../skills/results_ellaboration/results-paper-readiness-gatekeeper/SKILL.md) | canonical | instruction-only |
| `skills:results-prior-art-disqualifier-auditor` | [results-prior-art-disqualifier-auditor](../../skills/results_ellaboration/results-prior-art-disqualifier-auditor/SKILL.md) | canonical | instruction-only |
| `skills:results-proof-packet-deriver` | [results-proof-packet-deriver](../../skills/results_ellaboration/results-proof-packet-deriver/SKILL.md) | canonical | instruction-only |
| `skills:results-theorem-scope-certifier` | [results-theorem-scope-certifier](../../skills/results_ellaboration/results-theorem-scope-certifier/SKILL.md) | canonical | instruction-only |
| `skills:routea-collar-redesign-forger` | [routea-collar-redesign-forger](../../skills/results_ellaboration/routea-collar-redesign-forger/SKILL.md) | canonical | instruction-only |
| `skills:routea-continuum-gap-gatekeeper` | [routea-continuum-gap-gatekeeper](../../skills/results_ellaboration/routea-continuum-gap-gatekeeper/SKILL.md) | canonical | instruction-only |
| `skills:routea-endpoint-error-budget-certifier` | [routea-endpoint-error-budget-certifier](../../skills/results_ellaboration/routea-endpoint-error-budget-certifier/SKILL.md) | canonical | instruction-only |
| `skills:routea-endpoint-local-integral-calculator` | [routea-endpoint-local-integral-calculator](../../skills/results_ellaboration/routea-endpoint-local-integral-calculator/SKILL.md) | canonical | instruction-only |
| `skills:routea-finite-margin-evaluator` | [routea-finite-margin-evaluator](../../skills/results_ellaboration/routea-finite-margin-evaluator/SKILL.md) | canonical | instruction-only |
| `skills:routea-geometric-coefficient-extractor` | [routea-geometric-coefficient-extractor](../../skills/results_ellaboration/routea-geometric-coefficient-extractor/SKILL.md) | canonical | instruction-only |
| `skills:routea-geometric-collar-builder` | [routea-geometric-collar-builder](../../skills/results_ellaboration/routea-geometric-collar-builder/SKILL.md) | canonical | instruction-only |
| `skills:routea-margin-endpoint-certifier` | [routea-margin-endpoint-certifier](../../skills/results_ellaboration/routea-margin-endpoint-certifier/SKILL.md) | canonical | instruction-only |
| `skills:routea-open-point-orchestrator` | [routea-open-point-orchestrator](../../skills/results_ellaboration/routea-open-point-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:routea-paper-attack-orchestrator` | [routea-paper-attack-orchestrator](../../skills/results_ellaboration/routea-paper-attack-orchestrator/SKILL.md) | canonical | instruction-only |
| `skills:routea-paper-result-integrator` | [routea-paper-result-integrator](../../skills/results_ellaboration/routea-paper-result-integrator/SKILL.md) | canonical | instruction-only |
| `skills:routea-same-theory-factorization-hunter` | [routea-same-theory-factorization-hunter](../../skills/results_ellaboration/routea-same-theory-factorization-hunter/SKILL.md) | canonical | instruction-only |
| `skills:routea-same-theory-normalization-certifier` | [routea-same-theory-normalization-certifier](../../skills/results_ellaboration/routea-same-theory-normalization-certifier/SKILL.md) | canonical | instruction-only |
| `skills:routea-second-wave-manuscript-integrator` | [routea-second-wave-manuscript-integrator](../../skills/results_ellaboration/routea-second-wave-manuscript-integrator/SKILL.md) | canonical | instruction-only |
| `skills:routea-symbolic-cas-auditor` | [routea-symbolic-cas-auditor](../../skills/results_ellaboration/routea-symbolic-cas-auditor/SKILL.md) | canonical | instruction-with-helpers |
| `skills:review-reasoner` | [review-reasoner](../../skills/review/review-reasoner/SKILL.md) | canonical | instruction-only |
| `skills:review-reasoner-concept-logician` | [review-reasoner-concept-logician](../../skills/review/review-reasoner-concept-logician/SKILL.md) | canonical | instruction-only |
| `skills:review-reasoner-discovery-scientist` | [review-reasoner-discovery-scientist](../../skills/review/review-reasoner-discovery-scientist/SKILL.md) | canonical | instruction-only |
| `skills:review-reasoner-epistemologist` | [review-reasoner-epistemologist](../../skills/review/review-reasoner-epistemologist/SKILL.md) | canonical | instruction-only |
| `skills:review-reasoner-fields-medalist` | [review-reasoner-fields-medalist](../../skills/review/review-reasoner-fields-medalist/SKILL.md) | canonical | instruction-only |
| `skills:review-reasoner-radical-designer` | [review-reasoner-radical-designer](../../skills/review/review-reasoner-radical-designer/SKILL.md) | canonical | instruction-only |
| `skills:ym-audit-frontier` | [ym-audit-frontier](../../skills/yang_mills/ym-audit-frontier/SKILL.md) | canonical | instruction-only |
| `skills:ym-build-gauge-covariant-rg` | [ym-build-gauge-covariant-rg](../../skills/yang_mills/ym-build-gauge-covariant-rg/SKILL.md) | canonical | instruction-only |
| `skills:ym-build-observable-core` | [ym-build-observable-core](../../skills/yang_mills/ym-build-observable-core/SKILL.md) | canonical | instruction-only |
| `skills:ym-build-representation-calculus` | [ym-build-representation-calculus](../../skills/yang_mills/ym-build-representation-calculus/SKILL.md) | canonical | instruction-only |
| `skills:ym-calibrate-restricted-models` | [ym-calibrate-restricted-models](../../skills/yang_mills/ym-calibrate-restricted-models/SKILL.md) | canonical | instruction-only |
| `skills:ym-categorical-hott-physics-bridge` | [ym-categorical-hott-physics-bridge](../../skills/yang_mills/ym-categorical-hott-physics-bridge/SKILL.md) | canonical | instruction-with-helpers |
| `skills:ym-control-large-fields-and-topology` | [ym-control-large-fields-and-topology](../../skills/yang_mills/ym-control-large-fields-and-topology/SKILL.md) | canonical | instruction-only |
| `skills:ym-define-relational-rigidity` | [ym-define-relational-rigidity](../../skills/yang_mills/ym-define-relational-rigidity/SKILL.md) | canonical | instruction-only |
| `skills:ym-design-infrared-basin` | [ym-design-infrared-basin](../../skills/yang_mills/ym-design-infrared-basin/SKILL.md) | canonical | instruction-only |
| `skills:ym-design-regulator-atlas` | [ym-design-regulator-atlas](../../skills/yang_mills/ym-design-regulator-atlas/SKILL.md) | canonical | instruction-only |
| `skills:ym-freeze-clay-target` | [ym-freeze-clay-target](../../skills/yang_mills/ym-freeze-clay-target/SKILL.md) | canonical | instruction-only |
| `skills:ym-mechanize-proof-core` | [ym-mechanize-proof-core](../../skills/yang_mills/ym-mechanize-proof-core/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-adaptive-block-domination` | [ym-prove-adaptive-block-domination](../../skills/yang_mills/ym-prove-adaptive-block-domination/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-basin-entry` | [ym-prove-basin-entry](../../skills/yang_mills/ym-prove-basin-entry/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-conditional-partition-ratio` | [ym-prove-conditional-partition-ratio](../../skills/yang_mills/ym-prove-conditional-partition-ratio/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-continuum-coherence` | [ym-prove-continuum-coherence](../../skills/yang_mills/ym-prove-continuum-coherence/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-rg-to-rigidity` | [ym-prove-rg-to-rigidity](../../skills/yang_mills/ym-prove-rg-to-rigidity/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-rigidity-transfer` | [ym-prove-rigidity-transfer](../../skills/yang_mills/ym-prove-rigidity-transfer/SKILL.md) | canonical | instruction-only |
| `skills:ym-prove-state-weighted-defect-transfer` | [ym-prove-state-weighted-defect-transfer](../../skills/yang_mills/ym-prove-state-weighted-defect-transfer/SKILL.md) | canonical | instruction-only |
| `skills:ym-reconstruct-os-gap` | [ym-reconstruct-os-gap](../../skills/yang_mills/ym-reconstruct-os-gap/SKILL.md) | canonical | instruction-only |
| `skills:ym-run-clay-program` | [ym-run-clay-program](../../skills/yang_mills/ym-run-clay-program/SKILL.md) | canonical | instruction-only |

## Excluded reference sources

These entries are accounted for but never installed or exposed as canonical operations.

| Source | Disposition |
| --- | --- |
| `.prism/portable-repository-adoption-plan/source/project-skills/repository-adoption/portable-repository-adopter/SKILL.md` | request-local-reference |
| `abducer-prism/examples/conversion_input/source/.agents/skills/release-review/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/claude/.claude/skills/review/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/codex/.agents/skills/review/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/epistemic-diagnosis/.agents/skills/diagnose/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/mixed/.agents/skills/portable/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/mixed/.claude/skills/shared/SKILL.md` | fixture |
| `abducer-prism/tests/fixtures/opencode/.opencode/skills/audit/SKILL.md` | fixture |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/audit-reasoning-run/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/detect-essential-fragmentation/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/diagnose-categorical-defect/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/evaluate-relevance/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/falsify-candidate/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/formalize-candidate/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/generate-theory-candidates/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/instantiate-concretely/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/interpret-conceptual-pressure/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/map-theory-fragment/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/mutate-representation/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/profile-concept-meaning/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/propose-theory-morphism/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/prove-transport/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/run-philosophical-reflection/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/scope-research-context/SKILL.md` | vendored |
| `agentic/external/higher_abductive_theory_discovery/2026-07-22/active_snapshot/skills/synthesize-portfolio/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-audit-frontier/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-build-gauge-covariant-rg/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-build-observable-core/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-build-representation-calculus/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-calibrate-restricted-models/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-control-large-fields-and-topology/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-define-relational-rigidity/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-design-infrared-basin/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-design-regulator-atlas/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-freeze-clay-target/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-mechanize-proof-core/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-basin-entry/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-continuum-coherence/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-rg-to-rigidity/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-rigidity-transfer/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-reconstruct-os-gap/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-run-clay-program/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-audit-frontier/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-build-gauge-covariant-rg/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-build-latex-paper/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-build-observable-core/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-build-proof-appendix/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-build-representation-calculus/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-calibrate-restricted-models/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-control-large-fields-and-topology/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-define-relational-rigidity/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-design-infrared-basin/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-design-regulator-atlas/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-develop-paper-proofs/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-draft-finite-block-certificate/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-draft-frustration-obstruction/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-draft-heat-kernel-enclosures/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-draft-representational-dynamics/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-draft-staple-dispersion/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-frame-paper-narrative/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-freeze-clay-target/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-ground-paper-literature/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-mechanize-proof-core/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-adaptive-block-domination/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-basin-entry/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-conditional-partition-ratio/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-continuum-coherence/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-rg-to-rigidity/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-rigidity-transfer/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-prove-state-weighted-defect-transfer/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-reconstruct-os-gap/SKILL.md` | vendored |
| `agentic/external/yang_mills_representational_dynamics/2026-07-21/active_snapshot/11_vscode_codex_skill_bundle/.agents/skills/ym-run-clay-program/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-abductive-mechanism-hypothesizer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-area-concept-trace-builder/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-candidate-ranker/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-concept-formalizer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-conceptual-creativity-reasoner/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-conceptual-crisis-formalizer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-dialectic-explainer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-discovery-signal-miner/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-domain-adapter/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-failure-classifier/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-field-tension-elicitor/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-full-explanation-builder/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-graph-trace-serializer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-input-typology/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-mechanism-counterfactual-critic/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-mechanism-requirements-formalizer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-mechanism-todo-elicitor/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-obligation-verifier/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-retrospective-evolution-formalizer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-solver-orchestrator/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-task-evidence-curator/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-tension-evidence-cartographer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-transformation-proposer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-use-case-motivation-writer/SKILL.md` | vendored |
| `external/hegelian-solver/agents/hegelian-web-expansion-scout/SKILL.md` | vendored |
