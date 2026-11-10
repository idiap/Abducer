---
name: results-elaboration-workflow-orchestrator
description: Orchestrate the independent result-elaboration workflow for a paper draft. Use when a draft with expansion markers must be interpreted, converted into extension needs, planned as self-contained TODOs, assigned to paper-specific skills, and connected to local workflow hooks without invoking discovery workflows.
---

# Results Elaboration Workflow Orchestrator

## Workflow

Run this workflow independently from discovery marathon execution:

1. Invoke `results-context-interpreter` on the draft.
2. Invoke `results-extension-need-extractor` on every result slot, placeholder, author checklist, and marked gap. If the draft uses explicit open modules rather than slots, invoke `results-open-module-decomposer`.
3. Invoke `results-extension-strategy-planner` to order needs into self-contained TODOs with slot-specific validation criteria, limitation-addressed notes, paper insertion targets, and stop criteria.
4. For theorem-shaped or paper-subgoal candidates, invoke the recurring certification stack:
   - `results-theorem-scope-certifier` to state the smallest honest theorem and non-claims;
   - `results-finite-object-formalizer` when a new parameter, obstruction, certificate, quotient, residual set, or local object controls the proof;
   - `results-proof-packet-deriver` to prove, block, or demote the scoped theorem;
   - `results-prior-art-disqualifier-auditor` before novelty or contribution language;
   - `results-paper-readiness-gatekeeper` before manuscript handoff.
5. Invoke `results-critical-self-refiner` to separate deterministic checks from generative proof work and reject generic or overclaiming TODOs.
6. Invoke `results-narrative-integrator` to specify how discharged results enter the explanatory paper narrative.
7. Invoke `results-expansion-validator` to audit marker coverage, claim boundaries, local hooks, and narrative coherence.

## Deterministic Path

For TeX drafts, use the local analyzer:

```bash
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/analyze_result_expansion.py /path/to/draft.tex
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_result_expansion_report.py agentic/reports/results_ellaboration/<slug>/latest.json
```

For TeX drafts with `openmodule` environments, use the open-module analyzer:

```bash
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/analyze_openmodule_expansion.py /path/to/draft.tex
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_openmodule_expansion_report.py agentic/reports/results_ellaboration/<slug>/latest.json
```

To implement the generated TODOs into an expanded manuscript-facing draft:

```bash
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/compute_three_hairpin_certificate.py
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_result_todos.py /path/to/draft.tex
```

For the Route A SU(2) three-hairpin draft, integrate and cite the supplied verification script with:

```bash
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/verify_routea_three_hairpin_block.py
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/integrate_routea_certificate.py /path/to/finite_wilson_os_routeA_SU2.tex
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_routea_openmodule_todos.py agentic/reports/results_ellaboration/<slug>/finite_wilson_os_routeA_SU2_certificate_integrated.tex
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/implement_routea_paper_attack_todos.py agentic/reports/results_ellaboration/<slug>/finite_wilson_os_routeA_SU2_narrative_enriched.tex
```

For second-wave Route A open-point work, keep the work inside the paper-result workflow and use:

```bash
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/validate_routea_edge_paths.py agentic/reports/results_ellaboration/<slug>/routea_path_validation_example.json
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/render_routea_path_diagram.py agentic/reports/results_ellaboration/<slug>/routea_path_validation_example.json
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/check_schur_factor_candidates.py
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/evaluate_routea_finite_margins.py
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/derive_routea_endpoint_incidence.py agentic/reports/results_ellaboration/<slug>/routea_path_validation_example.json
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/certify_routea_endpoint_error_budget.py --fixture positive
.venv-pmp/bin/python skills/results_ellaboration/results-elaboration-workflow-orchestrator/scripts/integrate_routea_second_wave_results.py /path/to/paper.tex
```

The implementation path must preserve claim boundaries. If the source draft lacks regulator-specific Wilson data, implement a rigorous finite certificate or an explicit demotion boundary rather than promoting an unsupported Wilson theorem.

## Codex Exec Protocol

Every deterministic run must be followed by generative interpretation. Treat script outputs as evidence artifacts, not as paper claims by themselves. After running an analyzer, validator, certificate checker, path validator, margin evaluator, endpoint certifier, or TeX integrator, inspect the emitted JSON/Markdown/TeX path, state the epistemic status of the mathematical object, and name the validation handoff or unresolved obligations before editing the manuscript.

## Hook Boundary

Read [references/workflow-hooks.md](references/workflow-hooks.md) before adding hooks. Hooks are local checkpoints in this workflow only. They must not modify `hooks/hooks.json`, discovery-marathon jobs, branch schedulers, target active pointers, or long-horizon discovery queues.

## Paper Project Namespace

Keep paper outputs project-specific. The generic timeline-paper paths such as `agentic/reports/timeline_paper/latest.tex` and `agentic/reports/timeline_paper/latest.pdf` are compatibility pointers for the most recent build only; they must not be treated as the durable home of a manuscript. After any timeline-paper build, archive and validate the result under `agentic/reports/paper_projects/<paper-project-id>/` so distinct projects can coexist.

Use stable IDs tied to the paper claim, not the workflow run. For example, P vs NP transfer-obstruction work belongs under `p-vs-np-transfer-obstruction-certificate`, while Yang-Mills Wilson/OS work belongs under its own Yang-Mills project directory. Result-elaboration packets should point back to the project manifest when it exists and must not copy another target's terminology, report sections, or bibliography into the current paper project.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

For recurring paper-subgoal certification, do not advance from "near paper note" to "paper handoff" until theorem scope, central finite objects, proof packet, prior-art boundary, disqualifier matrix, and paper-readiness gate are all explicit. This applies across domains: P vs NP method-class no-go theorems, Yang-Mills finite obstruction packets, and any future result candidate extracted from a long-horizon timeline.

## Output Contract

Return: source draft, context summary, extracted needs or open modules, ordered TODOs, deterministic/generative regime split, critical self-refinement review, limitation review, implemented manuscript artifacts when requested, skill map, local workflow hooks, narrative integration plan, report paths, validation status, unresolved obligations, and next manuscript action.

## Failure/Demotion

Demote the workflow if it cannot find expansion markers, if the TODOs are not self-contained, if it routes into discovery workflows, if it overclaims beyond the draft's claim boundary, or if it lacks narrative integration.
