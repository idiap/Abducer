
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Function

This skill uses a transparent recommendation model:

`Potential(h) = 0.21*S + 0.14*C + 0.14*E + 0.16*L + 0.12*G + 0.08*A + 0.07*T + 0.08*N`

`Risk(h) = 0.45*R + 0.22*C_neg + 0.18*B + 0.15*U`

`Score(h) = clip(Potential(h) * (1 - 0.55*Risk(h)) + 0.05*V, 0, 1)`

Signal meaning:

- `S`: support signal from hypothesis evaluation.
- `C`: positive global coherence contribution.
- `E`: explanatory power.
- `L`: structural leverage from entrypoints/interventions/pathways.
- `G`: strategy leverage from strategy + proof-sketch artifacts.
- `A`: anti-barrier alignment from hardness diagnostics.
- `T`: testability (validation protocol + falsifier quality).
- `N`: novelty/fertility.
- `R`: refutation signal.
- `C_neg`: negative coherence pressure.
- `B`: barrier pressure.
- `U`: uncertainty (`1 - confidence`).
- `V`: revision-priority bonus if the hypothesis touches revision-loop targets.

Design principle:

The function intentionally rewards hypotheses that are simultaneously promising and executable, while penalizing high-risk but under-specified routes.

Bridge-first companion model:

`BridgePriority(b) = 0.28*B + 0.22*C_b + 0.24*P_b + 0.14*H_b + 0.12*R_b`

Where:

- `B`: bridge-program strength from `bridge-plan`.
- `C_b`: conjecture maturity from abstraction priority.
- `P_b`: proof-sketch quality.
- `H_b`: linked hypothesis support.
- `R_b`: proof readiness from obligations, lemmas, outline steps, and falsifiability hooks.

Design principle:

The final expert report should explain bridges before it recommends hypotheses. Hypotheses matter insofar as they support, sharpen, or undermine the bridge objects and proof architectures.

