<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning predicate map

This system-level ERFL projection collapses each detailed `steps` expression
to its ordered, duplicate-free predicate signature. The domain is a named
reasoning program; the range is its named calibrated output. Only that output
connects to downstream reasoning programs.

```text
map abducer {
  reasoning::target_navigation_loop -requires> output::target_navigation_loop.target_status
  output::target_navigation_loop.target_status -> reasoning::abducer_work_loop
  output::target_navigation_loop.target_status -> reasoning::release_promotion_loop
  reasoning::discovery_marathon_loop -constrain, probe, test, calibrate> output::discovery_marathon_loop.discovery_status
  output::discovery_marathon_loop.discovery_status -> reasoning::release_promotion_loop
  output::discovery_marathon_loop.discovery_status -> reasoning::conceptual_hypothesis_exploration_loop
  output::discovery_marathon_loop.discovery_status -> reasoning::target_navigation_loop
  reasoning::abducer_work_loop -assume, test, calibrate> output::abducer_work_loop.work_status
  output::abducer_work_loop.work_status -> reasoning::release_promotion_loop
  output::abducer_work_loop.work_status -> reasoning::conceptual_hypothesis_exploration_loop
  output::abducer_work_loop.work_status -> reasoning::target_navigation_loop
  reasoning::conceptual_hypothesis_exploration_loop -constrain, transfer, assume, test, calibrate> output::conceptual_hypothesis_exploration_loop.refinement_status
  output::conceptual_hypothesis_exploration_loop.refinement_status -> reasoning::abducer_work_loop
  output::conceptual_hypothesis_exploration_loop.refinement_status -> reasoning::release_promotion_loop
  reasoning::release_promotion_loop -requires> output::release_promotion_loop.release_status
  output::release_promotion_loop.release_status -> reasoning::target_navigation_loop
  output::release_promotion_loop.release_status -> reasoning::conceptual_hypothesis_exploration_loop
  reasoning::evidence_to_proof_route_onramp -constrain, assume, calibrate, revise, test> output::evidence_to_proof_route_onramp.calibrated_route
  output::evidence_to_proof_route_onramp.calibrated_route -> reasoning::theorem_proof_delivery
  output::evidence_to_proof_route_onramp.calibrated_route -> reasoning::conceptual_hypothesis_exploration_loop
  reasoning::conceptual_frontier_deepening -constrain, test, calibrate, revise, assume> output::conceptual_frontier_deepening.calibrated_candidate
  output::conceptual_frontier_deepening.calibrated_candidate -> reasoning::theorem_proof_delivery
  output::conceptual_frontier_deepening.calibrated_candidate -> reasoning::conceptual_hypothesis_exploration_loop
  reasoning::theorem_proof_delivery -test, calibrate> output::theorem_proof_delivery.calibrated_proof_status
  output::theorem_proof_delivery.calibrated_proof_status -> reasoning::scientific_contribution_cultivation
  output::theorem_proof_delivery.calibrated_proof_status -> reasoning::conceptual_hypothesis_exploration_loop
  reasoning::scientific_contribution_cultivation -test, calibrate> output::scientific_contribution_cultivation.calibrated_contribution
  output::scientific_contribution_cultivation.calibrated_contribution -> reasoning::manuscript_result_elaboration
  reasoning::manuscript_result_elaboration -constrain, test, calibrate> output::manuscript_result_elaboration.calibrated_manuscript
  output::manuscript_result_elaboration.calibrated_manuscript -> reasoning::theorem_proof_delivery
  reasoning::deep_review_and_reorientation -constrain, calibrate> output::deep_review_and_reorientation.calibrated_reorientation
  output::deep_review_and_reorientation.calibrated_reorientation -> reasoning::target_navigation_loop
  output::deep_review_and_reorientation.calibrated_reorientation -> reasoning::conceptual_hypothesis_exploration_loop
  reasoning::timeline-paper-independent-workflow -requires> output::timeline-paper-independent-workflow.paper_status
  output::timeline-paper-independent-workflow.paper_status -> terminal
  reasoning::ym-representational-dynamics-overlay -requires> output::ym-representational-dynamics-overlay.overlay_status
  output::ym-representational-dynamics-overlay.overlay_status -> terminal
  reasoning::cohere_fast -requires> output::cohere_fast.calibrated_domain_result
  output::cohere_fast.calibrated_domain_result -> reasoning::cohere_fast_scope_and_ground
  reasoning::cohere_fast_scope_and_ground -requires> output::cohere_fast_scope_and_ground.scope_status
  output::cohere_fast_scope_and_ground.scope_status -> reasoning::cohere_fast_adaptive_frontier
  reasoning::cohere_fast_adaptive_frontier -requires> output::cohere_fast_adaptive_frontier.frontier_status
  output::cohere_fast_adaptive_frontier.frontier_status -> reasoning::cohere_fast_derivation_and_proof
  reasoning::cohere_fast_derivation_and_proof -requires> output::cohere_fast_derivation_and_proof.derivation_status
  output::cohere_fast_derivation_and_proof.derivation_status -> reasoning::cohere_fast_independent_audit
  reasoning::cohere_fast_independent_audit -calibrate> output::cohere_fast_independent_audit.audit_status
  output::cohere_fast_independent_audit.audit_status -> reasoning::cohere_fast_manuscript_release
  reasoning::cohere_fast_manuscript_release -requires> output::cohere_fast_manuscript_release.release_status
  output::cohere_fast_manuscript_release.release_status -> terminal
}
```

The map hides occurrences, ports, skills, artifacts, and runtime order. It
preserves relation names, output identity, terminality, and cross-reasoning
connections. A predicate list summarizes structure; it does not assert that
every predicate applies directly between the source program and its output.
