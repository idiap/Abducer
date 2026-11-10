<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Test: Gedanken Experiment Design Quality

This file defines forward tests for the Gedanken skill cluster. The tests are qualitative oracles for Codex or API-driven runs; they complement JSON packet validation by checking whether the generated design is actually useful.

## Universal Quality Oracle

A passing answer must include:

- A need decision among `design_now`, `run_concrete_probe_first`, `defer_until_variable_typed`, `defer_until_regime_typed`, `quarantine_as_analogy`, and `not_needed`.
- A controlled contrast with one varied variable and explicit held-fixed controls.
- An expected observation and at least one disconfirming observation.
- A counterfactual variant whose predicted change is diagnostic.
- A transfer verdict, what transfers, what does not transfer, and a certificate needed.
- A follow-up task with success and failure or demotion criteria.
- A statement that the thought experiment is not proof progress without later validation.

## Case 1: Spectral Leakage Bridge

Prompt: A branch claims that exponential decay of a Euclidean two-point function should imply a positive Hamiltonian gap, but the observable family and reconstruction map are only partly typed. Decide whether to design a Gedanken experiment.

Expected decision: `design_now`.

Oracle: The design should isolate whether low-energy spectral weight can hide from the chosen observable family. It should hold fixed OS positivity, the reconstructed Hilbert space, and gauge-invariant observable typing. It should vary observable density or support of the spectral measure. It should ask for a transfer certificate from Euclidean correlator decay to the Hamiltonian spectral measure.

## Case 2: Fixed-Regulator Transfer Claim

Prompt: A branch has a clean finite-volume lattice calculation and wants to treat it as continuum evidence without uniform cutoff control.

Expected decision: `defer_until_regime_typed` or `run_concrete_probe_first`.

Oracle: The answer should not design an attractive story around the finite regulator. It should demand typed order of limits or a concrete uniformity probe first. Any imagined situation must identify noncommuting limits as the central failure mode.

## Case 3: Pairwise Positivity Route

Prompt: A branch has pairwise positivity checks and wants to infer full reflection positivity for a finite family of observables.

Expected decision: `design_now`.

Oracle: The design should vary the family size or Gram matrix structure while holding the positivity cone definition fixed. The disconfirming observation should be a finite-family obstruction where pairwise positivity persists but the full quadratic form fails.

## Case 4: Analogy-Only Carrier

Prompt: A branch proposes using a mechanical oscillator analogy to infer a mass gap in a target theory but cannot map variables, observables, or regimes.

Expected decision: `quarantine_as_analogy`.

Oracle: The answer should preserve the analogy as optional intuition but block graph promotion and active queue priority. It should state what transfer certificate would be needed before revival.

## Case 5: Non-Yang-Mills Queueing System

Prompt: A service system has rising arrival rate, bounded service capacity, and an observed queue-length divergence near saturation. Decide whether a thought experiment can clarify whether the divergence is linear, nonlinear, or threshold-like.

Expected decision: `design_now` or `run_concrete_probe_first` if a closed-form probe is available.

Oracle: The answer should isolate arrival rate, service rate, utilization, and queue length; hold the scheduling policy and arrival distribution fixed; vary utilization; predict monotone or divergent behavior; and state when the result transfers to the operational system.

## Validation Notes

Run these cases through the five-skill cluster and then validate any produced packets:

```bash
python agentic/scripts/validate_skill_depth.py
python agentic/scripts/validate_gedanken_experiment_packets.py
```

A run fails this generative test if it produces fluent narrative without controlled variables, disconfirming observations, transfer limits, or follow-up queue criteria.
