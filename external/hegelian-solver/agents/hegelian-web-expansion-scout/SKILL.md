---
name: hegelian-web-expansion-scout
description: "Decide whether web search is required, recommended, unnecessary, or forbidden for a Hegelian solver case, then plan and integrate source expansion into the reasoning flow. Use when an input mentions current facts, recent developments, named historical events, source-sensitive claims, missing provenance, disputed chronology, external evidence, laws, standards, products, papers, organizations, or when a retrospective evolution case needs factual expansion beyond supplied text."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Web Expansion Scout

## Overview

Decide when external search is epistemically necessary and convert web findings into bounded evidence, not free-floating narrative. This skill supports retrospective cases and any solver path where material adequacy depends on sources outside the local input.

## Decision Rules

Use `required` when:

- the user asks for latest, current, recent, today, or source links;
- the claim may have changed: products, APIs, laws, leaders, prices, standards, schedules, benchmarks, models, papers, or deployments;
- high-stakes legal, medical, financial, safety, or policy accuracy matters;
- a retrospective case names real events, people, organizations, dates, priority claims, or causal claims without adequate sources;
- downstream validation depends on primary sources, measurements, benchmark results, or release notes.

Use `recommended` when:

- supplied prose is plausible but thin on dates, citations, or counterevidence;
- multiple historical interpretations may exist;
- source quality will materially change confidence or graph branching;
- the case would benefit from primary-source anchoring but can still be treated as provisional without it.

Use `not_needed` when:

- the input is formal, hypothetical, toy, or fully source-contained;
- the user asks only for internal restructuring or schema conversion;
- local refs/files already supply enough evidence for the requested scope.

Use `forbidden_by_user` when the user explicitly says not to search.

## Search Plan

When search is required or recommended, produce:

- target claims to verify;
- preferred source classes: primary papers, official docs, standards, archived release notes, datasets, credible histories, or direct institutional records;
- query strings with date or domain constraints when helpful;
- acceptance criteria for source reliability;
- stopping criteria: enough independent source support, direct contradiction found, or source scarcity acknowledged.

## Integration Flow

1. Start from `input_intake_packet` or a draft `retrospective_evolution_packet`.
2. List claims that need external support; do not search vague background when a precise claim can be checked.
3. Search and collect sources only for those claims.
4. Convert findings into evidence records with URL, title, source class, publication or event date, claim supported, reliability, and uncertainty.
5. Update the concept or retrospective packet:
   - add evidence refs;
   - revise dates or transition ordering;
   - split branches when sources disagree;
   - add assumptions and unknowns where evidence is insufficient.
6. Record search provenance and residual source limits in the reasoning log.

## Output

Return:

```yaml
web_expansion_plan:
  decision: required | recommended | not_needed | forbidden_by_user
  reasons: []
  target_claims: []
  search_queries: []
  preferred_sources: []
  reliability_criteria: []
  stopping_criteria: []
  integration_targets: []
  no_search_boundary: string | null
web_evidence_packet:
  evidence:
    - id: string
      type: retrieved_document | official_doc | paper | standard | dataset | archive | news | other
      url: string
      title: string
      source_class: string
      publication_date: string | null
      claim_supported: string
      reliability: low | medium | high | primary | official | unknown
      uncertainty: {}
      notes: []
  contradictions: []
  residual_limits: []
```

## Epistemic Discipline

- Prefer primary and official sources for factual claims.
- Keep source summaries short and traceable; do not over-quote.
- Distinguish source-backed facts from interpretive reconstructions.
- Treat absence of evidence as an uncertainty, not a disproof.
- Surface conflicts between sources as branch pressure for the concept graph.
