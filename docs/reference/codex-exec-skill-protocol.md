<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Codex Exec Skill Protocol

This protocol is the standard handoff between deterministic repo tools and generative mathematical interpretation. A script-backed skill should use it when execution can ground the answer without violating the user request or writing unsafe state.

## Five-Step Protocol

1. Context check: name the target, input artifacts, expected output, missing prerequisites, and whether the user asked for analysis only.
2. Deterministic run: execute the smallest relevant script or validator and record the exact command.
3. Artifact inspection: read the produced JSON, Markdown, log, or state file before drawing conclusions.
4. Generative interpretation: state the mathematical consequence, epistemic status, uncertainty, and what the artifact does not prove.
5. Typed next action: return a promotion, revision, evidence task, quarantine, rejection, or stop recommendation with unresolved obligations.

## When Not To Run

Do not run scripts when required inputs are absent, when writes would be unsafe or unrelated to the user request, when artifacts are known stale and cannot be refreshed, when the user explicitly requests analysis only, or when deterministic execution would hide a needed mathematical judgment.

## Required Output Fields

- `executed_commands`: exact command strings or `none`.
- `produced_artifacts`: repo-relative paths inspected or `none`.
- `mathematical_consequence`: what changed about definitions, invariants, route obligations, or proof relevance.
- `epistemic_status`: conjectural, evidence-backed, proof-obligation, blocked, refuted, promoted, or quarantined.
- `unresolved_obligations`: missing definitions, counterexamples, proof steps, source evidence, or validators.
- `next_action`: the smallest controlled follow-up.

## Examples

Discovery skill: run a discovery-cycle script, inspect candidate rankings, then report which generated hypotheses preserve target commitments, which disconfirming observations would demote them, and which route enters proof queue versus watch/archive.

Evaluation skill: run the relevant validator or audit script, inspect hard-gate results, then separate preserved invariants from broken invariants and convert failures into proof obligations or demotion reasons.

Reporting skill: generate the report artifact only after source artifacts exist, inspect the report for preserved epistemic status, then state which claims remain conjectural, blocked, or evidence-backed.
