<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Public reasoning trace examples

These compact examples describe the semantic content expected from emitters. Field names follow the public trace contract; production events also include run identity, event identity, ordering, workflow coordinates, and artifact digests.

## Complete inference

```json
{
  "event_family": "inference",
  "question": "Does the candidate route preserve the theorem's quantifiers?",
  "premises": [
    {"type": "exact_statement", "claim": "For every finite instance, the bound is uniform in n."},
    {"type": "route_obligation", "claim": "The bridge must preserve uniformity."}
  ],
  "operator": "quantifier-preservation-check",
  "warrant": "The bridge lemma is uniform in n and introduces no instance-dependent constant.",
  "conclusion": "The route preserves the finite theorem statement.",
  "evidence": [{"relation": "supports", "artifact_id": "lemma.bridge.4"}],
  "claim_epistemic_status": "supported",
  "scope": {"regime": "finite", "model": "declared-source-model"},
  "authority": {"epistemic_upgrade": false}
}
```

The event supports a scoped conclusion. It does not promote the result to an asymptotic or continuum theorem.

## Failure and demotion

```json
{
  "event_family": "inference",
  "question": "Can the route cross from the finite model to the continuum regime?",
  "operator": "regime-shift-audit",
  "warrant": "No uniform limiting estimate is present in the supplied artifacts.",
  "conclusion": "Demote the route to finite-only evidence.",
  "alternatives": [{"claim": "Continuum promotion", "disposition": "rejected"}],
  "falsifiers": [{"condition": "A cutoff-uniform estimate is certified", "effect": "reopen"}],
  "claim_epistemic_status": "scope_limited",
  "workflow_disposition": "quarantined"
}
```

## Gate and handoff

```json
{
  "event_family": "gate",
  "gate": {
    "decision": "handoff",
    "required_authority": "proof-quality-gate",
    "open_obligations": ["formalize the endpoint case"]
  },
  "handoff": {
    "to_workflow": "scientific_contribution_cultivation",
    "artifact_type": "ResultAtlasSlice",
    "accepted": true
  },
  "claim_epistemic_status": "proved_in_declared_scope",
  "workflow_disposition": "handed_off"
}
```

## Integrity-valid but conjectural

```json
{
  "artifact_validation_status": "integrity_valid",
  "claim_epistemic_status": "conjectural",
  "workflow_disposition": "retained_for_testing",
  "authority": {"epistemic_upgrade": false}
}
```

The green digest receipt proves which bytes were reviewed. It does not prove that the claim is correct or novel.

## Trace incomplete

```json
{
  "event_family": "inference",
  "trace_status": "trace_incomplete",
  "conclusion": "Legacy artifact records a route selection.",
  "missing_requirements": ["typed premises", "public warrant", "rejected alternatives"],
  "workflow_disposition": "observability_gap"
}
```

An adapter may preserve this historical fact but must not reconstruct the missing rationale.

## Blind adjudication

During adjudication, candidates use pseudonymous IDs and no author, skill, or agent identity is rendered. The mapping is attached only to a causally later post-decision audit event. A renderer or fixture that reveals the mapping before the decision fails the epistemic-safety gate.
