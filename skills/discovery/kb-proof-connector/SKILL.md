---
name: kb-proof-connector
description: Build a relational graph over KB statements and identify the highest-informative intervention points for proof discovery. Use when the user asks to connect definitions/theorems/axioms, discover high-value bridge links, prioritize abductive targets, map proof pathways, or surface concept/method/barrier structure across `KB/*.kb.md`.
---

# KB Proof Connector


## Conceptual Role

This skill analyzes a KB as a structured relational graph and proposes the highest-value connections, intervention points, and proof hypotheses.

## Framework Contribution

It contributes the core connective tissue of the framework by exposing potential support links, inferential commitments, and bridge-worthy concept structure.

## How To Read Outputs

Read its outputs as candidate inferential moves and conceptual intervention points that still require downstream coherence, deduction, or hypothesis testing.

## Overview

Analyze the KB as a dependency graph plus semantic relation graph to rank where new connections would produce the highest proof payoff.

Read [references/scoring-model.md](references/scoring-model.md) for scoring details.
Read [references/script-usage.md](references/script-usage.md) for execution commands.
Read [references/prompt-template.md](references/prompt-template.md) when generating narrative interpretations.

## Workflow

1. Load target KB graph.
Parse statement YAML blocks and build directed edges from `depends_on`.

2. Quantify graph structure.
Compute components, downstream impact, bridge centrality, and unresolved dependencies.

3. Propose cross-component links.
Generate candidate links between statements in disconnected regions using lexical overlap and math-aware semantic features (symbol-role alignment, method overlap, theorem-family overlap, equivalence/reduction, definitional expansion).

4. Build concept graph.
Emit concept/method/barrier nodes and typed relations (`defines`, `uses`, `generalizes`, `obstructs`, `analogy_to`, `reexpresses`).

5. Rank intervention points.
Score each statement by proof-impact potential and produce top priorities.

6. Prepare abductive loop seeds.
Export top intervention targets and top candidate links for iterative abduction/deduction cycles and conceptual hypothesis synthesis.

## Guardrails

- Treat proposed links as hypotheses, not established dependencies.
- Preserve statement IDs exactly as they appear in KB.
- Prefer sparse, high-value links over dense low-signal link sets.
- Surface missing dependencies explicitly.

## Output Contract

Return:

1. `Stats`
2. `Top Intervention Points`
3. `Top Connection Candidates`
4. `Concept Graph`
5. `Abductive Loop Plan`

Use `scripts/analyze_kb_graph.py` for deterministic output artifacts.

<!-- ABducer skill-depth contract v1 -->

## Guardrails

- Novelty is not value; generated hypotheses must carry status labels and disconfirming observations before receiving active attention.
- Cite KB IDs, dependency node IDs, target packet IDs, artifact paths, validator output, or explicit unknowns for every substantive claim.
- Keep workflow validity, artifact existence, and mathematical progress as separate statuses.

## Mathematical Invariants

- Mathematical object: candidate bridge, conjecture, entrypoint, proof sketch, route family, or conceptual transformation.
- Preserved invariants: target commitments, source-grounded definitions, bridge compatibility, and explicit proof obligations.
- Name broken invariants, edge cases, counterexample classes, or boundary regimes whenever a route changes representation or scope.

## Epistemic Discipline

- Label claims as conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, quarantined, or watch/archive.
- Record uncertainty, source limits, disconfirming observations, and demotion triggers before recommending continuation.
- Treat explicit unknowns as first-class outputs rather than smoothing them into prose.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the answer. Run the relevant local script(s), especially `analyze_kb_graph.py, generate_phyp.py`; inspect the produced artifacts before interpreting them. After execution, state the mathematical consequence, epistemic status, unresolved obligations, and next action.

## Output Contract

Return: candidate route, mathematical object, cited source artifacts or unknowns, epistemic status, disconfirming observations, validation requirements, and next action. Include executed commands and produced artifacts when a deterministic run occurs; otherwise state why execution was not appropriate.

## Failure/Demotion

Demote to watch/archive, revision, quarantine, or reject when relevance is low, assumptions shift, source grounding disappears, or a counterexample/boundary regime breaks the route.

## Validation Handoff

End by naming the validator, artifact, TODO, proof obligation, or stop condition that should control the next loop. Do not leave shallow deterministic output uninterpreted when generative mathematical or epistemic interpretation is needed.
