<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning Monitor Runbook

The reasoning monitor is the visible observability surface for the Yang-Mills analysis loop. It communicates active target control, candidate route movement, evidence, uncertainty, stale-workflow isolation, and proof debt. It does not certify theorem progress by itself.

## Artifact

- HTML report: `agentic/reports/reasoning_monitor/latest.html`
- Data packet: `agentic/reports/reasoning_monitor/latest.json`
- Visual grammar: `docs/reference/reasoning-monitor-visual-grammar.md`
- Generative visual QA: `tests/generative/test_reasoning_monitor_visual_quality.md`

Open the HTML directly from the filesystem. It is designed to be self-contained: no external CSS, JavaScript, fonts, images, or server process are required.

## Refresh Sequence

Use the full gate before a serious analysis session:

```bash
python agentic/scripts/agentic_check.py
```

For a focused report refresh after target-navigation artifacts already exist:

```bash
python agentic/scripts/validate_active_target_workspace.py
python agentic/scripts/validate_skill_depth.py
python agentic/scripts/build_reasoning_event_log.py
python agentic/scripts/validate_reasoning_event_logs.py
python agentic/scripts/build_reasoning_monitor_packet.py
python agentic/scripts/generate_reasoning_monitor_html.py
python agentic/scripts/validate_reasoning_monitor.py
python agentic/scripts/run_long_horizon_probe.py
python agentic/scripts/validate_long_horizon_probe.py
python agentic/scripts/build_hamiltonian_gap_derivation.py
python agentic/scripts/generate_hamiltonian_gap_derivation_html.py
python agentic/scripts/validate_hamiltonian_gap_derivation.py
python agentic/scripts/build_physics_math_interpretation.py
python agentic/scripts/validate_physics_math_interpretation.py
```

## Reading The Lanes

- Target Spine: non-disposable commitments that every route must preserve.
- Dependency Frontier: open mathematical work, bridge obligations, and proof debt.
- Conceptual Pressure: generative pressure points where a frame, definition, or route needs transformation.
- Physics/Math Interpretation: active route interpretation that explains the mathematical object, physical meaning, proof mechanism, failure controls, and next lemma questions without relying on a relevance score.
- Hamiltonian Gap Derivation: mathematical expansion of the Hamiltonian spectral-gap route into Hilbert space, vacuum projection, spectral theorem, Euclidean decay, and continuum-stability obligations.
- Candidate Routes: controlled creative hypotheses with target relevance and drift risk.
- Validation Gates: hard checks, obligations, and disconfirming observations attached to candidates.
- Proof Debt: unresolved obligations. Treat this as the main warning surface.
- Evidence Ledger: concrete artifact paths that ground the dashboard claims.
- Drift Guard: stale-workflow and historical-artifact isolation.

## Status Semantics

- `evidence-backed`: grounded in listed artifacts, but not automatically a proof.
- `proof-obligation`: worth active attention only as an unresolved obligation.
- `conjectural`: creative or explanatory, not promoted until validation gates are met.
- `blocked`: cannot advance until a repair action is identified.
- `watch/archive`: keep for memory or later comparison, not long-horizon focus.

## Route Dispositions

- `proof_queue`: a candidate is worth converting into concrete proof obligations.
- `discovery_branch`: a candidate may expand the conceptual space but needs more evidence before proof work.
- `revision_loop`: the route should repair definitions, commitments, or framing before more proving.
- `watch/archive`: preserve as historical or comparative material.
- `proof_completion`: reserved for discharged obligations; do not infer this from visual polish.

## Operator Discipline

The first viewport should name `yang-mills-existence-and-mass-gap-target`, show commitments, frontier count, candidate count, proof obligations, and stale active findings. If the active target differs from `agentic/state/current_target.json`, the validator must fail.

When reviewing a route, inspect the cited commitments, target relevance score, drift risk, validation packet, disconfirming observations, obligations, and evidence paths. A route is valuable only if it preserves the target spine and converts conceptual creativity into explicit mathematical work.

Historical P vs NP or Hille-Yosida artifacts may appear only under drift or evidence context as historical material. They must never appear as active Yang-Mills state.
