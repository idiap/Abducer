<!--
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT
-->

# Routing Matrix

## Intent to Skill Route

| intent | trigger examples | route | stop condition |
|---|---|---|---|
| ingest | "extract from sources", "build KB" | latex-kb-ingest | KB schema violations unresolved |
| cohere | "cohere the KB", "build a coherent relational theory", "connect and score coherence" | kb-proof-connector -> kb-coherence-evaluator | No parseable statements in KB or missing phyp generation |
| connect | "connect statements", "find bridge points", "informative intervention points" | kb-proof-connector | No parseable statements in KB |
| coherence-eval | "coherence", "explanatory power", "global consistency" | kb-coherence-evaluator | Missing analysis/phyp/KB |
| interpretation-reports | "human readable report", "interpret reasoning process", "discovery summary" | kb-orchestrator/generate_interpretation_reports.py | Missing artifacts directory |
| process-graph | "reasoning graph", "typed process graph", "dynamic graph replay" | kb-orchestrator/generate_process_graph.py | Missing logs or artifacts directory |
| reasoning-dynamics | "reasoning dynamics", "inferential metrics", "reasoning dashboard" | kb-orchestrator/generate_process_graph.py -> kb-orchestrator/generate_reasoning_dynamics.py | Missing process graph evolution |
| entrypoints | "best conceptual entry points", "where to start", "highest leverage concepts" | kb-entrypoint-finder -> kb-entrypoint-pathfinder | Missing concept/analysis/phyp artifacts |
| hardness | "why this is hard", "epistemologically hard", "essential bottlenecks" | kb-epistemic-hardness | Missing integrated intermediate artifacts |
| bridge-plan | "bridge essential concepts", "connect intermediate results systematically" | kb-concept-bridge-planner | Missing entrypoints/pathways/hypotheses |
| conjecture | "conjecture bridge objects", "what abstraction fills this concept gap", "missing intermediate mathematical object" | kb-gap-abstraction-conjecturer | Missing bridge-plan or pathway/phyp artifacts |
| strategies | "different proof strategies", "novel strategy prompt" | kb-novel-proof-strategist | Missing bridge-plan artifact |
| proof-sketch | "outline a proof for this conjecture", "proof sketch mode", "what would the proof route look like" | kb-proof-sketcher | Missing conjecture/strategy/bridge artifacts |
| expert-paper | "turn final analysis into paper", "recommend hypotheses to experts", "scientific write-up from final artifacts" | kb-expert-paper-generator | Missing phyp or canonical KB artifacts |
| hypothesis-eval | "evaluate hypotheses", "test phyp", "which hypotheses are supported/refuted" | kb-hypothesis-evaluator | Missing phyp or KB artifact |
| hypothesis-loop | "iterate hypotheses", "refutation loop", "resolve tentative hypotheses" | kb-hypothesis-refutation-loop | Missing phyp or KB artifact |
| revision-loop | "revise ontology", "repair definitions", "switch regime" | kb-revision-loop | Missing hypothesis-loop output |
| explain | "explain theorem", "give intuition" | kb-explain | Missing prerequisite IDs |
| deduce | "what follows", "derive corollaries" | kb-deduce | Dependency closure incomplete |
| abduce | "best explanation", "missing premise" | kb-abduce | Contradiction with accepted facts if disallowed |
| induce | "generalize successful strategy", "infer reusable proof template", "abstract repeated bridge pattern" | kb-induce | No stabilized bridge/strategy/proof-sketch corpus |
| abductive-loop | "iterate abduction", "systematic proof pathway search" | kb-proof-connector -> kb-coherence-evaluator -> kb-abduce -> kb-deduce -> kb-hypothesis-evaluator -> kb-hypothesis-refutation-loop -> kb-revision-loop -> interpretation-reports -> process-graph -> reasoning-dynamics (repeat) | No score gain across one full round |
| pipeline | "run full loop", "end-to-end" | latex-kb-ingest -> kb-proof-connector -> kb-coherence-evaluator -> kb-entrypoint-finder -> kb-entrypoint-pathfinder -> kb-epistemic-hardness -> kb-concept-bridge-planner -> kb-gap-abstraction-conjecturer -> kb-novel-proof-strategist -> kb-proof-sketcher -> kb-hypothesis-evaluator -> kb-hypothesis-refutation-loop -> kb-revision-loop -> interpretation-reports -> process-graph -> reasoning-dynamics -> expert-paper | Any upstream hard failure |

## Pipeline Defaults

For `pipeline` requests, use this order unless user overrides it:

1. `latex-kb-ingest`
2. `kb-proof-connector`
3. `kb-coherence-evaluator`
4. `kb-entrypoint-finder`
5. `kb-entrypoint-pathfinder`
6. `kb-epistemic-hardness`
7. `kb-concept-bridge-planner`
8. `kb-gap-abstraction-conjecturer`
9. `kb-novel-proof-strategist`
10. `kb-proof-sketcher`
11. `kb-hypothesis-evaluator`
12. `kb-hypothesis-refutation-loop`
13. `kb-revision-loop`
14. `kb-orchestrator/generate_interpretation_reports.py`
15. `kb-orchestrator/generate_process_graph.py`
16. `kb-orchestrator/generate_reasoning_dynamics.py`
17. `kb-expert-paper-generator`
18. `kb-explain` (optional prompt-driven add-on)
19. `kb-deduce` (optional prompt-driven add-on)
20. `kb-abduce` (optional prompt-driven add-on)
21. `kb-induce` (optional prompt-driven add-on after `conjecture`, `strategies`, or `proof-sketch`)

## Escalation Rules

- If user asks for strict results, run `deduce` before `abduce`.
- If user asks for intuition first, run `explain` before formal inference.
- If user asks for intervention discovery, run `kb-proof-connector` before `kb-abduce`.
- If user asks for global theory fit, run `kb-coherence-evaluator` after `kb-proof-connector` and before retention decisions.
- If user asks for the connector plus immediate theory-fit formation in one step, classify to `cohere`.
- If user asks for a scientific write-up and expert hypothesis prioritization, run `expert-paper` after final analysis artifacts are available.
- If user asks to resolve `phyp` candidates, run `kb-hypothesis-evaluator` before `kb-hypothesis-refutation-loop`.
- If user asks where to start, run `kb-entrypoint-finder` before any inference loop.
- If user asks why the problem is hard, run `kb-epistemic-hardness` after entrypoint/pathway generation.
- If unresolved hypotheses remain concentrated after loop rounds, trigger `kb-revision-loop`.
- If ingest confidence is low, block induction until source coverage improves.
- If no bridge/strategy/proof-sketch family has stabilized, block induction and prefer `conjecture` or `strategies` instead.

## Logging Policy

- After any orchestrated run, generate a run-level reasoning-log index and check `missing_expected_agents`.
- If missing expected agents are non-empty, treat run as operationally incomplete and inspect stage logs before continuing.
