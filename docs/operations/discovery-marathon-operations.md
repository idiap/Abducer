<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Discovery Marathon Operations

The marathon workflow is now a compatibility executor beneath the canonical
theory-first discovery cycle. The canonical cycle controls current-literature
assimilation, high-risk intuition, isolated parallel maturation, reflective
synthesis, and the next-action schedule. The older marathon contributes durable
branch mechanics and reports, but it may invest research budget only in exact
branch IDs authorized by a verified canonical commit.

## Control Model

1. Initialize the canonical and legacy runtimes with the same exact target and
   run IDs, while keeping their transaction roots and state schemas separate.
2. Complete and commit the canonical parent cycle: current literature
   assimilation/rebase, high-risk intuition, parallel hypothesis maturation,
   and reflective parent/synthesis. Symbolic or simulation work is optional
   support requested after reflection.
3. Verify the canonical result projection against its immutable manifest,
   state, artifacts, hash-chained events, role-specific feedback edges, and
   current store generation.
4. Intersect canonical branch bindings, schedule identity bindings, validated
   parallel outcomes, and pending positive theory actions. Only those exact
   branch IDs enter the legacy scheduler; titles or lexical similarity never
   create a binding.
5. Run the authorized branch subset through legacy exploration, falsifier,
   evidence, obligation, review, reporting, and release mechanics. The broad
   historical skill set is advisory, not receipt-free release evidence.
6. Record concrete mathematical learning, not only route status.
7. For failed, demoted, quarantined, artifact-blocked, or repeated-blocker
   major cycle sets, build failure archaeology: explain why the physics and
   mathematics were hard, why the route failed, why the failure was not
   anticipated, and which prompt-level premortem heuristic should guard the
   next cycle.
8. Run visual conceptualization when a failed set, plateau, low-explanatory
   route, or opaque theorem mechanism needs deep reflection. The metaphor must
   preserve named formal and physical properties, expose distortions, and emit
   at most one audited route consequence before renewed branch selection.
9. Rebuild reports and the reasoning monitor so the user can inspect what changed.

## Canonical Theory Gate

Research mode requires an exact canonical cycle projection before branch
selection. A typical handoff is:

```bash
uv run python agentic/scripts/run_canonical_discovery_cycle.py \
  --request agentic/runs/reflective_discovery/<target>/<run>/requests/cycle-request.json \
  --state-root agentic/state/canonical_discovery_transactions \
  --output agentic/runs/reflective_discovery/<target>/<run>/cycles/cycle-000000000001-result.json

uv run python agentic/scripts/run_discovery_marathon.py \
  --resume \
  --run-id <run> \
  --execution-mode research \
  --canonical-theory-cycle agentic/runs/reflective_discovery/<target>/<run>/cycles/cycle-000000000001-result.json \
  --canonical-theory-state-root agentic/state/canonical_discovery_transactions
```

The projection target and run must equal the marathon identities. Its
generation must be the current canonical generation and, after the first
handoff, must continue the last consumed canonical generation. The verifier
rejects `latest`/`current` aliases, local-only literature, an altered manifest,
cross-target artifacts, a broken event chain, bookkeeping-only feedback, and a
schedule whose positive actions do not bind a validated canonical branch.

The canonical store defaults to
`agentic/state/canonical_discovery_transactions`; the legacy marathon keeps its
own store at `agentic/state/discovery_transactions`. They must not be pointed at
the same root because their states have different meanings. `--execution-mode
smoke` may omit the canonical projection for mechanical checks, but the emitted
gate is explicitly `smoke_non_authoritative` with no research, investment, or
promotion authority.

## Pivot Discipline

Persist while a subgoal remains target-linked and failures sharpen definitions, assumptions, equations, or bridge obligations. Backtrack when a result uses the wrong object, cutoff, reconstruction stage, or observable family. Pivot when repeated certified failures show that a route cannot protect the target commitments while another route can. Quarantine attractive analogies or empirical evidence until they have a transfer certificate.

Active preinvestment control: before a new avenue receives ordinary branch
exploration, proof lock-in, or long API marathon budget, it must pass the
literature-gap warrant described in
`docs/research-methods/literature-gap-preinvestment-gate-plan.md` and specified by
`agentic/spec/avenue_literature_gap_warrant.schema.json`. The warrant cites
closest known work, states the specific research gap, justifies relevance,
field impact, unification power, and route-decision power, and decides whether
the avenue may be invested in, limited to an artifact sprint, reframed, rejected
as prior-art collision, or quarantined. The deterministic gate is
`agentic/scripts/validate_avenue_literature_gap_warrant.py`; target-scoped
warrants live under `agentic/reports/avenue_literature_gap_warrants/targets/`.

## Validation

Every cycle must state candidate lemmas, assumptions, equations with validity conditions, attempted derivations, falsifiers, dependency updates, skill-dispatch traces, and a next experiment. The validators reject shallow cycles that only say to split a task, rerun a workflow, or continue generally.

For Yang-Mills cycles, the physical-relevance packet must also state
unification power: which separate physical carriers, Clay gates, estimates,
representations, or route pressures are compressed by one mechanism. A branch
without that compression remains support-only even when the local mathematics
is correct.

Failure archaeology is target-scoped under
`agentic/reports/failure_archaeology/targets/<target>/latest.json` and
`latest.md`. Generate it with
`python3 agentic/scripts/build_cycle_failure_archaeology.py --target <target>`
and validate it with
`python3 agentic/scripts/validate_cycle_failure_archaeology.py <packet.json>`.
Future cycle prompts include failed-hypothesis premortem signatures such as
`artifact_debt`, `proxy_shift`, `finite_to_global_gap`, `uniformity_gap`,
`definitional_transfer`, `no_falsifier`, `low_publication_reward`, and
`noncommuting_limits`.

Visual conceptualization is target-scoped under
`agentic/reports/visual_conceptualization/targets/<target>/latest.json` and
`latest.md`. Generate it with
`python3 agentic/scripts/build_visual_conceptualization_packet.py --target <target>`
and validate it with
`python3 agentic/scripts/validate_visual_conceptualization_packet.py <packet.json>`.
Visual metaphors are reflection artifacts only unless the preservation audit
promotes a concrete artifact, falsifier, route mutation, counterfactual variant,
or representation requirement. The default cap is one visual reflection pass per
failed major cycle set.

## Yang-Mills representational dynamics overlay

The Yang-Mills target has a target-scoped representational dynamics overlay:

- Target id: `yang-mills-existence-and-mass-gap-target`
- Source index: `agentic/reports/ym_representational_dynamics_integration/source_index.json`
- Proof objects: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/proof_objects/ym_representational_dynamics_objects.json`
- Overlay report: `agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/ym_representational_dynamics_overlay.html`
- Validator: `python3 agentic/scripts/validate_ym_workflow_integration.py`

Run the validator before any Azure marathon on this target. The overlay is a
restricted-theorem and workflow layer, not a Clay proof: every imported result
must carry claim level, hypotheses, non-claims, demotion trigger, and frontier
gate before it can affect branch routing.

For a one-cycle Azure/API marathon, set the outer job duration slightly above
the inner minimum-cycle floor; for example, use `--duration-seconds 3660` with
`--min-cycle-seconds 3600`. The wrapper reserves a launch margin, so an exact
`3600/3600` configuration is a no-op calibration check rather than a cycle
launch.

Broad API branch selection must never fill unused parallel slots with
artifact-blocked Yang-Mills endpoint branches. If target-specific
artifact-or-stop hints forbid broad API reasoning for a branch, the scheduler
should skip it and accept a smaller active set. If every available branch is
artifact-blocked, the preflight must block the broad marathon and route the next
work to an endpoint source-table artifact sprint, falsifier sprint, publication
demotion, or quarantine packet.
