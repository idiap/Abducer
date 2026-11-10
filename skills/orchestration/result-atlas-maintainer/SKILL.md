---
name: result-atlas-maintainer
description: Maintain Abducer's cumulative result and subgoal atlas. Use when a discovery workflow needs to persist achieved results, derivations, obstructions, falsifiers, bridge candidates, open obligations, target-specific problem-map status, or report-facing cumulative scientific memory across P vs NP, Yang-Mills, or other target runs.
---

# Result Atlas Maintainer

## Role

Use this skill when results must survive beyond a single timeline card. The goal is to turn reports, branch outputs, derivations, contribution candidates, and no-go/falsifier packets into durable subgoal-level objects.

## Procedure

1. **Preserve target identity.**
   Read `target_id` first. Refuse to merge artifacts from another target unless the artifact explicitly declares a matching target or is target-neutral infrastructure.

2. **Normalize result objects.**
   Convert each contribution, bridge, obstruction, derivation, falsifier, or milestone into a result entry with stable result id, subgoal id, result kind, claim, evidence, dependencies, validation state, open obligations, promotion criteria, demotion criteria, and non-claims.

3. **Map to problem space.**
   Place each result under target-specific route families. For P vs NP use families such as hardness magnification, natural-property/barrier analysis, MCSP/MKtP carrier transfer, proof-complexity transfer, padding/projection, and all-exponent uniformity. For Yang-Mills use finite OS obstruction, Wilson collar calculation, same-theory transfer, constructive continuum control, spectral reconstruction, and nontriviality witness.

4. **Separate achievements from intentions.**
   Mark entries as `achieved`, `partially_achieved`, `open`, `blocked`, `falsified`, `quarantined`, or `handoff_ready`. Do not mark a queued experiment as achieved unless evidence and validation state support it.

5. **Attach derivations.**
   Link definitions, assumptions, equations, proof steps, blocking gaps, and non-claims to result ids. Keep exact derivations separate from sketches, symbolic audits, and heuristic arguments.

6. **Update future control.**
   Feed the atlas back into branch prompts, queue ranking, and report rendering so future cycles know what is already known, what remains open, and which subgoals would produce the highest payoff.

## Epistemic Discipline

Every atlas entry must carry an epistemic status. Treat `open`, `blocked`, `partially_achieved`, `quarantined`, and `handoff_ready` as different states, not as stylistic labels. Evidence must cite source artifacts, cycle ids, branch ids, validator outputs, or derivation objects. A result is not promoted because it sounds important; it is promoted only when validation handoff and open obligations justify the status.

Track the mathematical invariant behind each subgoal: the target identity, route family, source object, target object, transfer condition, proof status, non-claim boundary, and failure or demotion evidence. If a future cycle changes one of these invariants, record a supersession or backtrack relation rather than overwriting the older result.

## Output Contract

Produce or update:

- `agentic/reports/result_subgoal_atlas/latest.json`
- `agentic/reports/problem_space_map/latest.json`
- `agentic/reports/derivation_vault/latest.json`
- matching Markdown reports
- validation handoffs and report links

## Codex Exec Protocol

When maintaining the atlas inside Codex, perform a deterministic run before generative interpretation whenever scripts are available:

```bash
python agentic/scripts/build_result_subgoal_atlas.py
python agentic/scripts/validate_result_subgoal_atlas.py
python agentic/scripts/build_problem_space_map.py
python agentic/scripts/validate_problem_space_map.py
python agentic/scripts/build_derivation_vault.py
python agentic/scripts/validate_derivation_vault.py
python agentic/scripts/update_subgoal_state_from_cycle.py
```

After the deterministic run, inspect the produced artifacts and explain the scientific meaning of changed subgoals, blocked nodes, derivation links, and validation gaps. Do not substitute generic prose for artifact inspection.

## Guardrails

- Do not collapse target-specific language into generic labels.
- Do not let P vs NP and Yang-Mills artifacts bleed into one another.
- Do not promote a result to handoff-ready without evidence, validation state, and non-claim boundary.
- Do not lose failed-branch learning; quarantined or falsified routes are still useful map entries.
