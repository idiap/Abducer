<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Epistemic Output Types

Reasoning types describe how epistemic state changes. Output types describe
what kind of object exists after that change, what authority it carries, and
how it may be consumed.

Artifact names and output types are deliberately separate. A LemmaChain is a
repository artifact type. Its semantic contents may include a conditional
Claim, several entails-given Relations, and unresolved proof Obligations.
Successful serialization of the artifact establishes none of those contents.

The initial machine-readable typology is
agentic/registries/epistemic_output_types.yaml.

## Primary output kinds

| Kind | Function | Direct substantive-claim effect |
|---|---|---|
| KnowledgeBase | Versioned epistemic graph under explicit scope, provenance, consistency, and revision policies | None; membership never promotes authority |
| Claim | Proposition capable of being true or false | May introduce or qualify a claim |
| Evidence | Inspectable item bearing on a claim | None without a typed relation |
| Decision | Epistemic adjudication or operational disposition | Calibration or gating only |
| Model | Explicit formal, symbolic, numerical, or idealized representation | None by itself |
| Relation | Typed connection among output identities | Relational warrant only |
| Obligation | Condition remaining before a specified use or promotion | Restricts authority |
| Plan | Prospective bounded reasoning or action | None until executed and assessed |
| Presentation | Communicative view over authoritative outputs | Permanently none |
| Bundle | Product, tagged alternative, collection, context, or handoff | Componentwise |

Every concrete output has one primary kind. A KnowledgeBase is a first-class
versioned object whose members retain their own identities and authority; it is
not merely a path to a Markdown file or an untyped context handle. A bundle can contain heterogeneous
members, but each member retains its own identity, modality, scope, provenance,
taints, and obligations.

For persistence, `KB/*.kb.md` is authoritative; proposed revisions remain
artifacts until validated writeback creates a successor version. Indexes,
graphs, reports, and reasoning logs are derived views or audit records, not
implicit KB updates.

## Common properties

Every output carries:

    output identity
    primary kind
    producing reasoning occurrence
    epistemic modality
    claim effect
    scope
    provenance
    taints
    open obligations
    mutability policy
    terminality
    admissible consumers

Semantic content is immutable. Revision produces a new output identity related
by revises, supersedes, or calibrates. Re-rendering a presentation does not
revise its source claims.

## Codomains of the essential reasoning types

| Reasoning type | Required output bundle |
|---|---|
| A | Candidate-explanation Claim, explains-candidate Relation, alternatives, falsification obligations |
| D | Conditional-entailment Claim, entails-given Relations to indispensable premises, proof obligations |
| I | Provisional-generalization Claim, generalizes-over Relations, boundary obligations |
| T | Candidate-transfer Claim, transfers-via Relation, preservation obligations |
| C | Contrast Claim, relevant Evidence, contrast Relations, boundary obligations |
| M | Model, model-finding Claim, models/idealizes Relations, robustness obligations |
| R: refuted | Counterexample Evidence, refutes Relation, refutation Decision |
| R: not refuted | Bounded search Evidence, nonrefutation Decision, remaining obligations; no positive Claim |
| E | Calibration Decision, calibrates Relation, state snapshot; no substantive Claim |

These signatures prevent common epistemic coercions:

- Deduction from an abductive candidate remains conditional on that candidate.
- A simulation trace is evidence about a model execution, not automatically
  about the target system.
- Not finding a counterexample within a bounded search produces a Decision and
  search trace, not a validated Claim.
- Calibration may classify, promote under a declared rule, demote, or gate an
  existing claim. It cannot invent evidence or a new object-level claim.
- Plans, handoffs, receipts, and presentations contribute no scientific
  authority merely by completing successfully.

## Semantic ports

ERFL can normally infer codomains from the reasoning occurrence. Where
interfaces would otherwise be ambiguous, ports use semantic constructors such
as:

    Observation<X>
    Candidate<X>
    Claim<X,Status>
    Evidence<X>
    Witness<X>
    Assessment<X>
    Calibrated<X>
    Obligation<X>
    Scope<X>
    Constraint<X>
    Delta<X>
    Goal<X>
    Unavailable<Reason>

Collections use T?, T*, T+, or T{m..n}. Tagged alternatives use A | B;
products requiring all members use A & B.

Unavailable is an operational inability to perform reasoning. It is not a
refutation, negative evidence, or an inconclusive scientific result. Delta<X>
represents a genuine epistemic change. Replaying the same output is not a delta
and cannot count as additional evidence or iteration progress.

## Artifact audit

The current repository exposes 59 produced labels across 74 named-workflow
skill occurrences, but their shared artifact schema leaves payload structure
unconstrained. The labels are nominal rather than semantic types.

The current cohere-fast schemas define five artifact structures, while six
declared workflow return types remain undefined. Its 30 YM skills all use
DomainEvidencePacket, which does not distinguish model construction,
derivation, refutation, audit, and presentation.

Public reasoning events type consumed evidence but do not yet bind their
conclusions to typed and digested output artifacts. Consequently, the complete
relation

    reasoning occurrence -> epistemic output -> materialized artifact

cannot yet be validated end to end.

The initial artifact mappings in the registry are therefore examples, not a
complete migration. Generic or unmapped artifacts remain non-executable at the
reasoning-projection layer.

## Axes that must remain separate

The framework should not collapse these into one status field:

    integrity status
    epistemic status
    proof status
    workflow disposition
    publication status
    programme claim level

For example, accepted, quarantined, stopped, and archived are workflow
dispositions. They do not state whether a claim is supported, refuted,
entailed, or merely not refuted within a bounded scope.
