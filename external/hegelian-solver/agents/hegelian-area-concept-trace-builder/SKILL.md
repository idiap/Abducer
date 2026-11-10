---
name: hegelian-area-concept-trace-builder
description: "Build an informal, natural-language retrospective trace of an area's key concepts and their evolution, from a topic name rather than already-supplied prose. Gathers evidence informally in NL, marks confidence and contested points, and uses targeted web search only for claims that need verification, dates, or freshness. Use when the user names a field, area, or set of key concepts (e.g. \"trace the evolution of cancer mechanism understanding\") and wants a conceptual history assembled, scoped, and evidenced before any formal staging happens."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Area Concept Trace Builder

## Overview

`hegelian-retrospective-evolution-formalizer` formalizes prose that already exists. This
skill produces that prose in the first place: given only an area name or a short list of
key concepts, it scopes the area, identifies the conceptual turning points worth tracing,
writes an informal account of each, and decides — claim by claim, not wholesale — when a
targeted web search is worth running before the account is asserted with confidence.

The output is a research note, not a finished formal object. It is deliberately informal:
plain-language summaries, honest confidence labels, and "general consensus, no single
citation" where that is the truth, rather than fabricated precision. It is the recommended
input to `hegelian-retrospective-evolution-formalizer` when the user wants the full solver
pipeline (stages, transitions, graph seeds) on top of it.

## Procedure

1. **Scope the area.** State what is in and out of scope in one or two sentences. An area
   like "cancer mechanism understanding" is too broad to trace exhaustively — pick the
   handful of conceptual shifts that actually changed what counted as an explanation or an
   intervention, not every paper or every detail.
2. **Identify key concepts/turning points.** List them in roughly chronological or
   logical order. Each one should be a *shift in understanding* (a new mechanism, a new
   unifying framework, a new intervention class that followed from a mechanistic insight),
   not just a named event.
3. **Draft each entry from existing knowledge first.** Write the informal summary, approximate
   period, and what tension/anomaly/evidence drove the shift from the previous entry, using
   what you already know. Do not invent citations, dates, or numbers you are not confident
   of — mark them as approximate or unknown instead.
4. **Triage claims for search**, using `hegelian-web-expansion-scout`'s decision rubric:
   - `required`: a precise date, named primary source, recent development, or high-stakes
     claim (e.g. a specific clinical outcome or approval) that the account currently asserts
     without grounding.
   - `recommended`: plausible but thin — would benefit from one or two corroborating sources.
   - `not_needed`: durable, widely established background (textbook-level consensus) where a
     search would not change the account.
   Do not search for everything; search for the specific claims that fail this test.
5. **Run targeted searches** for only the triaged claims, using narrow queries (named
   mechanism, named therapy class, named researcher/year if known) rather than broad topic
   queries. Prefer review articles, primary papers, and institutional sources (e.g. NCI,
   WHO, major journals) over general web pages.
6. **Integrate findings as informal evidence notes**, not full `Evidence` records: a
   one-line source description, what it supports, and a confidence label. Update the
   summary, period, or confidence of the entry it was checked for; do not silently overwrite
   an uncertain claim with a confident one unless the source actually settles it.
7. **Flag contested or unsettled points explicitly** rather than picking one account
   silently — competing mechanistic explanations or contested priority claims are signal,
   not noise, for downstream tension/discovery work.
8. **Recommend the next step**: hand off to `hegelian-retrospective-evolution-formalizer`
   (when the user wants formal stages/transitions/graph seeds), `hegelian-web-expansion-scout`
   (when open threads need deeper source work than this pass did), or `none` (when the
   informal trace itself was the deliverable).

## Output

Return:

```yaml
area_conceptual_trace:
  area: string
  scope_note: string
  key_concepts:
    - concept_id: string
      name: string
      approx_period: string | null
      summary: string
      shift_from_previous: string | null
      informal_evidence:
        - claim: string
          source_note: string
          confidence: high | medium | low
          web_search_used: true | false
      contested_or_uncertain: []
  open_threads: []
  recommended_next_step: retrospective_evolution_formalizer | web_expansion_scout | none
  assumptions: []
  unknowns: []
```

## Epistemic Discipline

- Confidence labels are about the claim, not the writing: `low` confidence stated plainly
  beats a confident-sounding sentence built on an unchecked assumption.
- Never fabricate a citation, date, or number. "General consensus, no single citation" and
  "approximate, not independently verified" are acceptable and expected entries.
- Treat competing explanations as branches to preserve, not a single story to flatten.
- Distinguish what a search actually confirmed from what it merely did not contradict.
- Keep this output informal on purpose — do not pre-formalize it into solver schema fields;
  that is `hegelian-retrospective-evolution-formalizer`'s job, with this trace as its input.
