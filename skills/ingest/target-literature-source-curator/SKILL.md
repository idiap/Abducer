---
name: target-literature-source-curator
description: Curate cited primary and expert sources for a target problem's historical and conceptual literature evolution. Use when a report needs to explain the major problem, where it came from, how the literature evolved, and which references justify each stage.
---

# Target Literature Source Curator

## Conceptual Role

Use this skill to build a source-backed reference spine for a target problem. The goal is not a decorative bibliography. The source set must explain how the problem became well-posed, why it is hard, what the main route families are, and how the active Abducer run inherits obligations from the literature.

## Source Selection Procedure

1. Identify the target problem and its official or canonical statement.
2. Separate source roles:
   - `problem_statement`: official formulation or authoritative statement.
   - `origin`: paper or book introducing the core object.
   - `axiomatic_bridge`: source defining the rigor standard or reconstruction bridge.
   - `physics_motivation`: source explaining why the phenomenon is expected.
   - `constructive_program`: source showing how rigorous construction is attempted.
   - `route_obstruction`: source or expert report naming what remains blocked.
3. Prefer primary papers, official problem statements, monographs, and expert surveys.
4. For each reference, record the claim it supports and the limitation it does not settle.
5. Reject sources that are speculative, uncited solution claims, broad popular summaries, or not tied to a target obligation.

## Mathematical Object

The mathematical object is a target-literature spine: a typed relation between the target problem, its canonical statement, historical source objects, rigor standards, proof obligations, and cited reference records. Preserve the target object, the cited claim, the limitation, and the supported workflow implication for every source.

## Epistemic Discipline

Assign status labels: `canonical`, `primary`, `expert_survey`, `context_only`, `prior_art_risk`, or `exclude`.

Every source must have an evidence citation: URL or local path, reference id, role, supported claim, and limitation. Do not cite a reference as proof of the target unless it actually proves the target.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when a deterministic report exists. Run `python agentic/scripts/build_target_literature_evolution.py`, inspect `agentic/reports/target_literature_evolution/latest.json`, then run `python agentic/scripts/validate_target_literature_evolution.py` before relying on the packet in a report.

## Output Contract

Return:

1. `Target`: target id, problem name, and official statement source.
2. `Reference Spine`: cited records with role, year, authors, title, venue, URL, supported claim, and limitation.
3. `Evolution Stages`: chronological stages, each tied to references and conceptual shift.
4. `Open Obligations`: what the literature leaves unresolved for the active workflow.
5. `Validation Handoff`: run `python agentic/scripts/build_target_literature_evolution.py` and `python agentic/scripts/validate_target_literature_evolution.py`.

## Failure/Demotion

Demote the packet if references are uncited, if the story uses generic history instead of target obligations, if speculative solution claims are treated as established literature, or if source limitations are omitted.
