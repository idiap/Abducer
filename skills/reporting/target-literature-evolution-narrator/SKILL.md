---
name: target-literature-evolution-narrator
description: Write an understandable, cited narrative explaining a target major problem and how the literature evolved around it. Use when a report or timeline needs a user-facing tab that connects the problem statement, historical stages, conceptual shifts, and active workflow obligations.
---

# Target Literature Evolution Narrator

## Conceptual Role

Use this skill after a cited reference spine exists. The output should help an expert or motivated reader understand why the target problem has its current shape, why the obvious routes are insufficient, and how the active discovery loop relates to the historical literature.

## Narrative Procedure

1. Start from the smallest exact target statement.
2. Explain the core object in plain mathematical-physics language.
3. Tell the literature evolution as conceptual shifts, not as a list of dates:
   - object introduced,
   - rigor standard clarified,
   - physical mechanism discovered,
   - lattice/constructive approaches developed,
   - remaining proof obligations isolated.
4. For every stage, name what became possible and what remained unresolved.
5. End by mapping the literature to the current Abducer route families and branch-control criteria.

## Mathematical Object

The mathematical object is an explanatory literature-evolution packet: a structured map from target statement to cited conceptual stages, open proof obligations, and workflow-routing consequences. It must preserve the target problem, cited stage claims, source limitations, and same-target boundary.

## Epistemic Discipline

Assign epistemic status labels: `source_backed_context`, `interpretive_synthesis`, `open_obligation`, `active_route_relevance`, or `do_not_claim`.

Keep three things separate: what the literature proves, what it motivates, and what Abducer is currently exploring. Never imply that physical consensus, lattice evidence, or formal setup proves the Clay target.

Every narrative claim needs an evidence citation through a reference id, URL, local source path, report artifact, or explicit unknown. Mark uncited interpretive connections as provisional synthesis.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when updating the timeline report. Run `python agentic/scripts/build_target_literature_evolution.py`, validate with `python agentic/scripts/validate_target_literature_evolution.py`, regenerate `python agentic/scripts/generate_discovery_marathon_html.py`, and then run `python agentic/scripts/validate_discovery_marathon_report.py`.

## Output Contract

Return:

1. `Problem In One Page`: accessible statement, why it matters, and what would count as a solution.
2. `Literature Evolution`: chronological conceptual stages with cited references.
3. `What The Literature Teaches The Workflow`: route obligations, pitfalls, and useful abstractions.
4. `Open Problems Still Alive`: construction, nontriviality, OS/Wightman adequacy, continuum limit, and mass gap.
5. `References`: compact cited bibliography with URLs.
6. `Validation Handoff`: report artifact plus validator.

## Failure/Demotion

Demote if the narrative is a generic encyclopedia summary, has no citations, hides unresolved obligations, treats numerical or lattice evidence as proof, or fails to connect the literature to current workflow decisions.

## Validation Handoff

Use `python agentic/scripts/build_target_literature_evolution.py`, `python agentic/scripts/validate_target_literature_evolution.py`, and the discovery-marathon HTML validator.
