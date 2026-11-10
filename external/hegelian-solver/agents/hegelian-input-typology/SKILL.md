---
name: hegelian-input-typology
description: "Classify incoming Hegelian solver material by input kind, modality, temporal scope, domain hints, evidence state, web-search need, and downstream route. Use at the start of a solver run when the user provides raw text, files, URLs, structured concepts, examples, failures, traces, graph artifacts, historical narratives, or mixed evidence bundles and the workflow needs to decide which skills should run next."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Input Typology

## Overview

Turn heterogeneous user material into an `input_intake_packet` that tells the solver what kind of work is being requested and which skill path should handle it.

## Input Kinds

Classify the dominant input as one or more of:

- `structured_concept`: YAML/JSON concept node, physical concept, language-model concept, or generic schema.
- `prose_seed`: informal definition, theory sketch, model description, or system description.
- `field_tension_request`: a request to elicit, sharpen, or formalize a tension, controversy, crisis, dilemma, or unresolved opposition in a field.
- `retrospective_evolution_text`: prose about how a concept, theory, technology, practice, or institution developed in the past.
- `area_trace_request`: a request to build a retrospective conceptual trace of a named field, area, or set of key concepts, where the user has *not* already supplied the historical prose — the trace itself has to be researched and written, not just formalized.
- `evidence_bundle`: examples, counterexamples, measurements, benchmark logs, proof fragments, tool traces, source excerpts, or papers.
- `trigger_packet`: explicit failure certificates, anomaly lists, or discovery signals.
- `candidate_packet`: proposed transformations, successor concepts, validation packets, or rankings.
- `graph_or_trace`: previous concept graph, solver trace, reasoning log, report, or run ledger.
- `use_case_manifest`: batch of cases to validate or run.
- `report_request`: request to explain, summarize, render, compare, or audit an existing run.
- `live_or_current_claim`: claim whose truth may depend on current facts, releases, laws, prices, leaders, standards, or recent publications.

## Procedure

1. Record source modality: `text`, `file`, `url`, `structured_data`, `code`, `image`, or `mixed`.
2. Record temporal scope:
   - `static`: self-contained formal object or local artifact.
   - `retrospective`: past evolution is central.
   - `current_or_live`: current facts may matter.
   - `mixed`: historical baseline plus live status or current evidence.
3. Extract domain hints: mathematical, physical, language-model, software, institutional, scientific, product, or unknown.
4. Identify the epistemic state: source-backed, underspecified, internally inconsistent, date-sensitive, provenance-poor, or deliberately hypothetical.
5. Decide routing:
   - Use `hegelian-area-concept-trace-builder` for `area_trace_request` (no prose supplied
     yet — research and write the trace first), then optionally
     `hegelian-retrospective-evolution-formalizer` on its output if formal stages are wanted.
   - Use `hegelian-retrospective-evolution-formalizer` directly for `retrospective_evolution_text`
     (prose already supplied).
   - Use `hegelian-field-tension-elicitor`, `hegelian-tension-evidence-cartographer`, and `hegelian-conceptual-crisis-formalizer` for `field_tension_request`.
   - Use `hegelian-web-expansion-scout` when current facts, external history, missing provenance, or source verification may affect the graph.
   - Use the normal domain-adapter and concept-formalizer path for self-contained concept inputs.
6. Preserve ambiguity. Multiple input kinds can be true; choose a primary route and list secondary routes.

## Web Need Heuristics

Mark `web_expansion.decision` as:

- `required` when the request asks for latest/current facts, source verification, named real-world history without sources, legal/medical/financial/safety claims, or precise source attribution.
- `recommended` when the narrative has sparse dates, disputed priority claims, missing primary sources, named people/organizations, or likely important context outside the provided text.
- `not_needed` when the input is self-contained, toy/formal, already source-backed enough for the requested abstraction, or the user asked not to browse.
- `forbidden_by_user` when the user explicitly disallows web use.

## Output

Return:

```yaml
input_intake_packet:
  primary_input_kind: string
  secondary_input_kinds: []
  source_modality: string
  temporal_scope: static | retrospective | current_or_live | mixed
  domain_hints: []
  evidence_state: []
  downstream_route: []
  web_expansion:
    decision: required | recommended | not_needed | forbidden_by_user
    reasons: []
    candidate_queries: []
  assumptions: []
  unknowns: []
```

## Epistemic Discipline

- Distinguish what the user supplied from what must be inferred.
- Do not treat historical narration as proof of causality; mark causal claims separately.
- Separate formal route choice from material evidence sufficiency.
- Name uncertainty, provenance gaps, and possible falsifiers.
