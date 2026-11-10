---
name: hegelian-full-explanation-builder
description: Build a full reader-facing explanation below a compact Hegelian solver run summary. Use when a report, trace, or candidate transition needs the dense one-paragraph summary expanded into grounded prose that names the source concept, concrete use, determinate limit, successor concept, preservation map, validation obligations, ranking decision, and residual work.
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Full Explanation Builder

## Purpose

Expand a compact solver summary into a readable explanation that helps a reader understand the big picture first, then what changed, why it changed, what was preserved, how the candidate was checked, and what remains open.

## Required Inputs

- `ReasoningLog.summary` or equivalent compact explanation text.
- `concept_formalization` step, especially role, tasks, formal analysis, material analysis, and epistemic profile.
- `failure_classification` and `discovery_mining` steps.
- `candidate_generation` step, especially selected candidate, target concept, resolution mechanism, preservation map, changed structure, expected obligations, and residual limits.
- `validation` step for obligation statuses.
- `ranking` step for final decision, score, and reasons.

## Procedure

1. Split the compact summary into separate readable points before expanding it.
2. Start with the big picture: why this kind of concept matters in its domain and what use case family it represents.
3. Name the source concept and its concrete use.
4. Define the source concept using its role, task goals, examples, and signature.
5. Name the determinate limit: the failure label, failed obligation, and witness if available.
6. Explain why the limit matters for the source concept's intended use.
7. Name any discovery signal that makes the successor direction non-arbitrary.
8. Name the selected successor concept and the operator that produces it.
9. Explain the transition in ordinary language using the candidate's `resolution_mechanism`.
10. Explain preservation using the `preservation_map` and declared preservation constraints.
11. Explain validation by separating passed obligations from open obligations.
12. Explain the ranking decision without overstating it: `provisional` remains a candidate repair, not a verified Aufhebung.
13. End with residual limits and what would have to be shown next.

## Style

- Prefer 5-8 short sections or paragraphs when the report needs the big picture.
- Use section headings when helpful: `Big Picture`, `What Breaks`, `Why This Successor`, `What Is Preserved`, `How It Was Checked`, and `How To Read The Result`.
- Keep one claim per paragraph.
- Use concrete concept names and task language before abstract Hegelian vocabulary.
- Introduce terms such as determinate limit, preservation, mediation, and successor only after the concrete artifact has been named.
- If the candidate is not accepted, say "candidate repair" or "proposed successor"; do not call it final.
- Keep JSON, signatures, and long artifact payloads outside the prose or behind collapsible report details.

## Output Shape

Return:

```yaml
summary_points:
  - string
full_explanation:
  sections:
    - title: string
      paragraphs:
        - string
explanation_terms:
  source_concept: string
  determinate_limit: string
  successor_concept: string
  mediation: string
  preservation: string
  validation_status: string
  residual_work:
    - string
```

## Guardrails

- Do not invent missing validation evidence.
- Do not hide open obligations.
- Do not collapse multiple candidate branches into one final history unless the ranking actually accepts one final successor.
- Do not quote raw JSON in the prose.
- Distinguish formal checks from material adequacy and epistemic uncertainty.
