---
name: scientific-contribution-paper-handoff
description: Turn a certified or near-certified contribution candidate into a scoped paper-argument handoff. Use when a subgoal has enough novelty, explanatory power, implications, and evidence to deserve a standalone note, section, workshop paper, method paper, negative-result note, or expert handoff while preserving unresolved main-target obligations.
---

# Scientific Contribution Paper Handoff

## Conceptual Role

Use this skill when a contribution candidate is `near_stepping_stone` or `publishable_handoff_ready`. The goal is not to inflate a subgoal into the main theorem. The goal is to package exactly what was learned, why it is new or useful, what it explains, what it implies, and what remains open.

Do not write a paper handoff merely because exploration payoff is high. The handoff needs hard-gate evidence: claim statement, evidence, novelty boundary, validation/disqualifier checks, and overclaim boundary.

## Paper Handoff Procedure

1. State the smallest honest title and claim.
2. Identify contribution type: bridge lemma, obstruction, method, conceptual reframing, benchmark/probe, or evidence synthesis.
3. Write the argument spine:
   - problem pressure,
   - contribution object,
   - main mechanism,
   - validation evidence,
   - implications,
   - disqualifiers checked,
   - unresolved obligations.
4. Separate paper-ready content from watch/archive content.
5. Add an anti-overclaim paragraph that protects the main target boundary.
6. Report missing hard gates when the candidate is only near-ready.
7. Keep all pipeline, marathon, and skill-control language out of the paper-facing sections.

## Epistemic Discipline

Status labels: `paper_scaffold`, `near_certified_note`, `certified_note`, `blocked_by_prior_art`, `blocked_by_validation`, or `do_not_write`.

Every claim needs evidence citations: KB IDs, cycles, equations, reports, validators, source artifacts, or explicit unknowns. A paper handoff is invalid if it hides unresolved proof debt.

## Output Contract

Return:

1. `Title And Claim`: smallest honest title, abstract claim, and contribution type.
2. `Argument Spine`: stepwise scientific argument.
3. `Novelty And Explanation`: what is new, what it explains, and what would be known without it.
4. `Implications`: next analyses, broader route portfolio, and possible external audience.
5. `Evidence Table`: claim-to-artifact mapping.
6. `Disqualifiers And Limits`: prior-art risk, proxy risk, validation gaps, and main-target boundary.
7. `Hard-Gate Status`: claim, evidence, novelty, validation, and overclaim gates.
8. `Draft Sections`: suggested sections for Markdown/LaTeX.
9. `Validation Handoff`: required monitor, prior-art pass, validator, or TODO before publication.

## Failure/Demotion

Demote to `do_not_write` if the claim is only workflow progress, if evidence is absent, if novelty is unqualified, if hard gates are missing without finite tasks, if prior-art risk is high and unsearched, or if the draft would imply the main theorem has been solved.

## Validation Handoff

Use `python agentic/scripts/build_scientific_contribution_monitor.py`, `python agentic/scripts/validate_scientific_contribution_monitor.py`, and, when a candidate is near-certified, `prior-art-importer` plus `kb-expert-paper-generator` or `kb-macro-proof-paper-writer`.
