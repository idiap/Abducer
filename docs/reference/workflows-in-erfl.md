<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workflow representations in ERFL

The repository's workflows are represented in the Essential Reasoning Flow Language (ERFL) as relations between reasoning-type occurrences—not as sequences of implementation skills. The canonical machine-readable index is `agentic/registries/reasoning_flow_catalog.yaml`; each indexed `.prism` file is independently parseable and coherence-checked. The [single-file flow reference](all-reasoning-flows.md) reproduces every complete ERFL source in catalog order.

## Reading the notation

```text
steps a:A[ground->hypothesis] -assume> ...
      d:D[hypothesis->claim] -test> ...
      r:R[claim->verdict] -calibrate> ...
      e:E[claim,verdict->status]
```

`A`, `D`, `R`, and `E` denote abduction, deduction, refutation, and epistemic calibration. Other available types are induction (`I`), analogy/transfer (`T`), modeling (`M`), and contrast (`C`). Ports inside brackets state which epistemic handles enter and leave each occurrence. Relations name the warranted transformation. `_` is an explicit projection gap: it preserves an unknown rather than assigning a reasoning type without evidence. Parentheses express parallel composition, `repeat` gives a finite local iteration bound, and guarded `switch` handlers expose cross-workflow control.

A trailing `...` joins the next physical line to the same logical statement.
Indentation is for alignment only, so deeply nested or long routes remain
readable without giving whitespace hidden control-flow meaning.

The one-line `goal "summary" -> state` form used by the catalog is only a
shorthand for simple goals. ERFL 0.3 also supports structured goal blocks with
named critic criteria, evidence obligations, constraints, and `all(...)` or
`any(...)` satisfaction policies. Thus a reasoning program can refer to individual review
conditions and preserve their dispositions instead of compressing a complex
goal into one natural-language sentence.

## Referencing and persisting a KB

A preamble can connect one specific KB; directional arrows inside reasoning
then distinguish consumption from persistence:

```text
erfl 0.3
@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))
reasoning yang_mills_kb_cycle {
  goal "calibrate proposed Yang-Mills KB changes" -> persisted
  steps r:R[kb0,proposal->verdict] -calibrate> e:E[proposal,verdict->status]
  r <-query- kb0
  e -persist-> kb0
  on e.persisted => accept
  on e.refuted => stop
}
```

The resource declaration is outside the reasoning body. `r <-query- kb0`
draws KB material into `r`; `e -persist-> kb0` writes a successor only after
calibration. `search` is also available for broader indexed retrieval.
Proposed revisions, generated artifacts, and reasoning logs remain outside the
KB until an explicit persistence edge is accepted.

## Canonical workflow views

| Workflow | ERFL abstraction | Conceptual function |
|---|---|---|
| `target_navigation_loop` | `_ -requires> E` | Calibrate a target and dependency frontier, then route work or release. |
| `discovery_marathon_loop` | `E -constrain> (A & I) -probe> (M & C) -test> R -calibrate> E` | Generate, probe, contrast, test, and calibrate bounded discovery candidates. |
| `abducer_work_loop` | `A -assume> D -test> R -calibrate> E` | Advance or close an active proof obligation. |
| `conceptual_hypothesis_exploration_loop` | `E -constrain> A -transfer> T -assume> D -test> R -calibrate> E` | Replace an obstruction with a mediated, testable route. |
| `release_promotion_loop` | `_ -requires> E` | Issue a claim-conserving promotion, repair, or rejection disposition. |
| `evidence_to_proof_route_onramp` | `E -constrain> A -assume> D -calibrate> E -revise> A -test> R -calibrate> E` | Turn evidence into a falsification-aware proof route. |
| `conceptual_frontier_deepening` | `E -constrain> A -test> R -calibrate> E -revise> T -assume> D -calibrate> E` | Seek a discriminating bridge ready for formal work. |
| `theorem_proof_delivery` | `D -test> R -calibrate> E` | Settle an exact theorem under explicit premises. |
| `scientific_contribution_cultivation` | `A -test> R -calibrate> E` | Determine which scientific contribution is supported. |
| `manuscript_result_elaboration` | `E -constrain> A -test> R -calibrate> E` | Produce a scope-safe, evidence-aligned manuscript. |
| `deep_review_and_reorientation` | `E -constrain> (R & A) -calibrate> E` | Compare defeaters and repairs to select reorientation or stop. |
| `timeline-paper-independent-workflow` | `_ -requires> E` | Produce a claim-bounded presentation of accumulated reasoning. |
| `ym-representational-dynamics-overlay` | `_ -requires> E` | Calibrate a Yang–Mills candidate within its continuum claim boundary. |
| `cohere_fast` | `_ -requires> E` | Coordinate an isolated, domain-bound path to independent calibration. |
| `cohere_fast_scope_and_ground` | `_ -requires> E` | Bind target, sources, domain, and claim ceiling. |
| `cohere_fast_adaptive_frontier` | `_ -requires> E` | Form a bounded domain frontier without promotion. |
| `cohere_fast_derivation_and_proof` | `_ -requires> E` | Retain open obligations in a conditional derivation packet. |
| `cohere_fast_independent_audit` | `R -calibrate> E` | Adversarially assess the domain derivation. |
| `cohere_fast_manuscript_release` | `_ -requires> E` | Authorize presentation without increasing claim authority. |

## Alias resolution

Task-facing names resolve to one canonical semantic flow. For example, `target-navigation-control-plane` and `p-vs-np-target-navigation-run` resolve to `target_navigation_loop`; `discovery-marathon-control-loop` resolves to `discovery_marathon_loop`; `conceptual-obstruction-refinement` resolves to `conceptual_hypothesis_exploration_loop`; and `cohere-fast` resolves to `cohere_fast`. The hyphenated aliases declared by each named-workflow contract resolve to the corresponding underscore-form IDs. Cohere-fast labels such as `cohere_fast:scope-and-ground` similarly resolve to their underscore-form canonical IDs.

The cohere-fast family also makes its isolated, guarded control path explicit: when its calibrated intake is ready, `cohere_fast` switches to `scope_and_ground`, then successful calibrated stages switch to `adaptive_frontier`, `derivation_and_proof`, `independent_audit`, and finally `manuscript_release`. Only `manuscript_release` may accept the result, so the parent cannot bypass the required audit and release stages. No member switches into an existing non-cohere workflow.

## Epistemic status

These representations are descriptive abstractions, not executable workflow replacements. Locally, every declared relation is checked for type compatibility and conserved handles. Globally, the bundle remains deliberately non-executable while source-to-type projections are incomplete, `_` gaps remain, or workflow-switch cycles lack a shared bound or well-founded progress rank. This distinction prevents a readable summary from being mistaken for a verified, lossless compilation of operational behavior.
