---
name: hegelian-tension-evidence-cartographer
description: "Map the evidence, commitments, regimes, stakeholders, sources, counterevidence, and uncertainty around an elicited field tension. Use after a tension has been surfaced and before formal crisis construction, especially when the tension depends on empirical studies, benchmarks, institutions, deployed systems, public policy, measurement practices, or contested material claims."
---
<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->

# Hegelian Tension Evidence Cartographer

## Overview

Build an evidence map that keeps formal commitments and material adequacy separate. This skill prevents the crisis formalizer from mistaking slogans, anecdotes, or proxy metrics for settled evidence.

## Procedure

1. Start from a `field_tension_elicitation_packet`.
2. List the claims that actually matter to the tension:
   - formal claims about definitions, constraints, equivalence, objective functions, or invariants;
   - empirical claims about observed outcomes, failures, incidents, measurements, or benchmarks;
   - institutional claims about incentives, accountability, adoption, access, or governance;
   - normative claims about what must be preserved or avoided.
3. Attach source classes to claims:
   - proof, dataset, benchmark, field study, RCT, case report, audit, incident report, official policy, standard, ethnography, expert judgment, affected-community testimony, or historical record.
4. Rate evidence state:
   - `strong`, `suggestive`, `conflicted`, `thin`, `missing`, `outdated`, or `regime_limited`.
5. Identify counterevidence and failed mediations:
   - compromises already tried;
   - metrics that paper over the tension;
   - domain restrictions that solve one side while losing the other;
   - cases that should be decisive but are missing.
6. Decide whether web expansion is required or recommended using `hegelian-web-expansion-scout` when sources are external or current.

## Output

Return:

```yaml
tension_evidence_map:
  tension_ref: string
  decisive_claims:
    - id: string
      claim: string
      claim_kind: formal | empirical | institutional | normative | historical | operational
      supports_pole: string | null
      evidence_state: strong | suggestive | conflicted | thin | missing | outdated | regime_limited
      source_refs: []
      uncertainty: {}
      possible_falsifiers: []
  evidence_gaps:
    - id: string
      missing_claim: string
      why_it_matters: string
      search_or_study_needed: string
  counterevidence: []
  failed_mediations:
    - id: string
      mediation: string
      why_it_fails: string
      preserved: []
      lost_or_collapsed: []
  regime_map:
    valid_regimes: []
    overextension_risks: []
  source_expansion:
    decision: required | recommended | not_needed | forbidden_by_user
    reasons: []
```

## Epistemic Discipline

- Do not rank a claim as strong merely because it is central.
- Keep stakeholder testimony, institutional record, and formal proof in distinct evidence lanes.
- Treat proxy metrics as evidence about the proxy until the bridge to the target construct is justified.
- Mark where evidence supports one pole but does not refute the other.
- Surface missing decisive tests as part of the crisis, not as an afterthought.
