---
name: subgoal-enablement-handoff-packager
description: Package an enablement audit for a completed subgoal into report, atlas, timeline, proof-queue, or paper-facing language. Use after completed-subgoal-enablement-auditor, contribution-value-assessor, result-atlas-maintainer, or proof-delivery workflows decide that a subgoal is achieved, handoff-ready, locally valuable, route-deciding, or overclaimed and the repository needs a self-explanatory handoff for the bigger problem.
---

# Subgoal Enablement Handoff Packager

## Role

Use this skill to turn an enablement judgment into durable, readable artifacts. The output should make it obvious how a completed subgoal relates to the bigger problem without implying that the bigger problem is solved.

This skill packages meaning; it does not certify mathematical truth. Certification must come from the source proof, validator, prior-art check, or proof-delivery gate.

## Epistemic Discipline

Preserve the source epistemic status: `enabled`, `partially_enabled`, `route_deciding`, `paper_handoff_ready`, `local_value_only`, `blocked`, `quarantined`, or `proxy_or_overclaim`.

Every packaged statement must cite evidence: artifact paths, KB IDs, cycle IDs, proof-object IDs, source artifacts, validation output, or explicit unknowns. Keep the mathematical object, target gate, residual blockers, and non-claims visible in the packaged text.

Do not upgrade an audit label. If the input says `local_value_only`, the handoff may explain its local value but must not call it enabling. If the input says `proxy_or_overclaim`, the handoff must make the demotion or quarantine boundary explicit.

## Inputs

Use one or more of:

- an enablement audit from `completed-subgoal-enablement-auditor`;
- a result atlas entry from `agentic/reports/result_subgoal_atlas/latest.json`;
- a proof object from a proof-delivery queue;
- a timeline-paper section or latest-step cycle range;
- a paper draft module or manuscript section;
- validation output from proof-quality, prior-art, or timeline validators.

## Packaging Targets

Choose the target surface before writing:

- `atlas_entry`: update durable scientific memory with enablement status and remaining blockers.
- `timeline_note`: explain why the completed subgoal matters in the chronology.
- `proof_queue_note`: convert enablement into the next proof object or demotion condition.
- `paper_section`: write paper-facing prose without pipeline jargon.
- `html_summary`: short visible report text for a dashboard tab.
- `todo_queue`: self-explanatory next items when enablement is partial.

## Handoff Procedure

1. Restate the completed subgoal in one sentence.
2. State the bigger-problem gate it affects.
3. Use the enablement class as the controlling label.
4. Write the causal link: "because X is now established, Y can now be attempted/packaged/validated/closed."
5. Separate enabled work from residual blockers.
6. Include non-claims that protect the main target boundary.
7. Add citations to artifact paths, cycle ids, proof-object ids, validators, or explicit unknowns.
8. Produce one surface-specific handoff block and one machine-readable field proposal.

## Wording Discipline

Use direct language:

- "This opens..." only when a named next proof or validation gate can consume it.
- "This supports..." when it improves a paper argument or explanation but does not discharge a gate.
- "This rules out..." when it is a falsifier, no-go theorem, or route-decision result.
- "This remains local..." when the result is useful but lacks target transfer.
- "This must not be used to claim..." before any main-theorem boundary.

Avoid:

- saying the target problem is solved;
- calling workflow completion mathematical enablement;
- hiding the residual blocker;
- replacing proof debt with narrative polish;
- losing the source artifact or proof-object id.

## Surface Templates

### Atlas Entry

Return fields:

- `enablement_class`
- `enabled_gate`
- `enablement_mechanism`
- `consuming_next_step`
- `residual_blockers`
- `non_claims`
- `evidence_sources`
- `recommended_achievement_status`
- `promotion_criteria`
- `demotion_criteria`

### Timeline Note

Write:

1. What changed at this completed step.
2. Which gate in the bigger problem it opens, narrows, or closes.
3. Which latest cycle/proof object supplies the evidence.
4. What the next cycle or proof object should do.

### Paper Section

Write:

1. a claim paragraph;
2. an evidence paragraph;
3. a "why this enables the larger program" paragraph;
4. a residual-obligation paragraph;
5. an anti-overclaim paragraph.

Keep paper-facing text free of skill names, marathon mechanics, and dashboard labels unless the paper is explicitly about the workflow.

### TODO Queue

Use self-explanatory items:

- `title`: imperative action tied to the enabled gate;
- `why_now`: why the completed subgoal makes this the right next item;
- `input_artifacts`: exact paths or ids;
- `success_condition`: observable close condition;
- `demotion_condition`: what would show the enablement claim was too strong;
- `next_skill`: skill or validator that should consume the item.

## Output Contract

Return:

1. `Packaging Target`: atlas, timeline, proof queue, paper, HTML, TODO, or mixed.
2. `Enablement Summary`: one paragraph with class, gate, mechanism, and next consumer.
3. `Surface Block`: ready-to-insert prose or fields for the chosen target.
4. `Machine-Readable Fields`: JSON-like field proposal.
5. `Evidence Map`: artifact paths and ids.
6. `Residual Blockers And Non-Claims`: explicit boundary.
7. `Validation Handoff`: validator, script, proof object, paper section, or queue update to run next.

## Failure/Demotion

Demote the handoff if the enablement class is absent, evidence is uncited, the next consumer is unnamed, residual blockers are hidden, or the text would make the completed subgoal sound like a proof of the full target.
