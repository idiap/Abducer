---
name: routea-open-point-orchestrator
description: Coordinate second-wave Route A SU(2) Wilson-block paper-result work after the paper-attack pass. Use when the attack-integrated paper has unresolved collar, normalization, margin, endpoint, or continuum handoff obligations and the next step must be selected without invoking discovery-marathon workflows.
---

# Route A Open Point Orchestrator

## Purpose

Use this skill after the Route A paper-attack pass has converted open modules into paper-native gates and demotions. Its job is to choose the next manuscript-result capability, not to run broad discovery.

## State Machine

Track the paper state as:

1. `finite_source_collision_current`: the finite SU(2) heat-kernel source-collision theorem remains the current claim.
2. `collar_redesign_candidate`: a new geometric family has been proposed but not validated.
3. `validated_collar_geometry`: edge-list support, reflection, footprint, and common-limit checks pass.
4. `same_theory_normalization`: every normalization factor is congruence, observable rescaling, or certified positive-kernel/reflected-Gram.
5. `geometric_coefficients`: \(H_k,K_k,R_{k,\delta}\) are derived from the same normalized collar block.
6. `margin_or_finite_certificate`: strict reduced margins or a bounded finite example are certified.
7. `endpoint_derivation`: endpoint variables, color factors, incidence, and estimator are derived from the same regulator.
8. `endpoint_two_sided_error`: two-sided error budget classifies the endpoint certificate.
9. `continuum_handoff`: remains gatekeeper-only until uniform same-theory estimates and an OS reconstruction theorem exist.

## Routing Rules

- If the current obstruction is the failed transverse collar, route to `routea-collar-redesign-forger`.
- If a candidate geometry exists, route to `validate_routea_edge_paths.py` and `render_routea_path_diagram.py`.
- If a geometry passes but normalization contains pair-dependent factors, route to `routea-same-theory-factorization-hunter`.
- If no collar exists but the paper needs a concrete finite example, route to `routea-finite-margin-evaluator`.
- If endpoint work is requested before validated paths exist, demote or restrict it to source-collision bookkeeping.
- If endpoint variables exist but errors are missing, route to `routea-endpoint-error-budget-certifier`.
- If continuum or spectral claims are requested before uniform estimates, route only to `routea-continuum-gap-gatekeeper`.

## Decision Vocabulary

Use exactly one decision per step:

- `attempt`: enough prerequisites exist to try a construction or calculation.
- `promote`: result can enter the paper as theorem, proposition, lemma, finite certificate, or appendix calculation.
- `demote`: result exposes a mathematical obstruction and should enter as a remark or bounded non-claim.
- `quarantine`: artifact is invalid or mixes regimes.
- `defer`: mathematically meaningful but blocked by upstream prerequisites.
- `integrate_no_claim_change`: paper can receive clarification without strengthening the claim.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: active open point, current state, selected skill or script, dependencies satisfied/missing, mathematical reason for the choice, expected artifact, paper insertion target, promotion/demotion condition, validation commands, and next handoff.

## Failure/Demotion

Demote if a step routes into discovery-marathon files, bypasses missing collar prerequisites, promotes finite positivity into continuum reconstruction, or emits a task-management paragraph instead of a mathematical result target.
