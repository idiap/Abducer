---
name: frontier-literature-assimilator
description: Refresh or resolve the newest validated target-scoped literature-search snapshot, bind it to an active theory state, compute source and conceptual deltas, and turn them into explicit theory, hypothesis, genealogy, and scheduling updates. Use before a major conceptual-discovery portfolio is opened, whenever a newer literature search completes, before novelty or contribution claims, or when branches may be stale, duplicated, contradicted, absorbed, or newly enabled by recent work.
---

# Frontier Literature Assimilator

## Role

Make literature feedback-effective in theory formation. Own the
refresh-to-assimilation handoff. Do not stop at a bibliography or novelty gate:
state what the newest admissible search changes in the ontology, mechanisms,
tensions, hypotheses, comparisons, and next actions.

Read [references/literature-assimilation-contract.md](references/literature-assimilation-contract.md)
before producing a durable packet.

## Required Inputs

Require the target ID, theory-state version, prior literature snapshot when one
exists, candidate search snapshots, active conceptual systems and hypotheses,
and the discovery charter. A usable search snapshot names its search completion
time, coverage cutoff, queries, sources searched, inclusion/exclusion policy,
source records, content digest, and coverage limitations.

A global `latest` path is not identity. Select the newest validated snapshot
whose target, scope, and state compatibility match the active theory. If no such
snapshot exists, return `refresh_required` or `local_only`; do not imply that a
live or comprehensive search occurred. You may map bounded local evidence
provisionally, but label `hypothesis_rebase_status: provisional_local_only`; it
cannot satisfy the active-investment literature gate.

## Workflow

### 1. Resolve the literature basis or open a refresh

Compare candidate snapshots by validated completion time, not file mtime. Verify
target identity, query provenance, digest, source accessibility, and coverage.
If one is current for the target and claim scope, freeze its
`literature_snapshot_id` and exact digest. If none is admissible, create a typed
refresh request instead of fabricating a basis.

Use `target-literature-source-curator`, `kb-prior-art-pass`,
`prior-art-importer`, `literature-gap-relevance-auditor`, and
`results-prior-art-disqualifier-auditor` for collection, import, gap judgment,
and result-level collision checks. This skill owns refresh orchestration and
assimilation; those leaf skills own collection, import, and local judgments.

### 2. Run differentiated search lanes when refresh is required

Commission independent bounded lanes for:

- closest known statements and constructions;
- recent frontier publications and preprints;
- negative results, impossibility theorems, and barriers;
- conceptual and terminological genealogy;
- adjacent-field mechanisms with possible invariant transport;
- dissenting formulations and minority explanations.

Give each lane a target and claim scope, query log, providers or indexes,
publication cutoff, inclusion/exclusion policy, resource budget, and immutable
receipt. Parallelize lanes when execution authority permits, but never issue the
same generic search under different names. Prefer primary sources for technical
claims. Deterministically deduplicate by work identity such as DOI, arXiv ID,
canonical title/authors, or explicit version lineage, then reconcile claims
rather than merely concatenating citations.

### 3. Validate and freeze the refreshed snapshot

Require lane completion times, coverage limitations, source versions,
correction or retraction status when available, content digests, and validator
receipts. Freeze the reduced target-scoped snapshot only after identity and
provenance pass. Otherwise retain `refresh_required` or `local_only`.

### 4. Compute the literature delta

Against the prior snapshot, classify added, removed, corrected, retracted,
superseded, newly relevant, and unchanged sources. Separate publication recency
from search recency: a newly found old theorem may matter more than a new paper.

### 5. Map sources into theory

Before emitting a theory mapping, lift every distinct exact claim into the
source-semantic claim layer. Bind the claim to its source identity, observed
version, correction or retraction state, source digest, and extraction
provenance. A source-level audit may provide an explicit `entails`,
`contradicts`, `leaves_open`, or `unresolved` warrant. Here `entails` means only
that the frozen audit asserts a theory-side consequence; it is not a verified
mathematical entailment.

When an explicit exact-version warrant is absent, retain the deterministic
lexical/status mapper as `bounded_lexical_fallback`. Do not silently upgrade it.
Record the matched terms or relation signals, and keep source truth, semantic
entailment, exhaustive coverage, novelty, and external validation false or
unavailable. A correction, supersession, or retraction invalidates the old
version's warrant and forces a rebuilt relation.

For every decision-relevant source, state which concept, assumption, mechanism,
barrier, comparator, proof obligation, or explanation it:

- supports, contradicts, absorbs, sharpens, reframes, transfers, or leaves open;
- makes newly expressible or newly implausible;
- connects to another route or field;
- forces into the conceptual genealogy.

Do not infer agreement from vocabulary overlap. Use exact statements and source
limitations.

Emit a coverage audit covering every decision-relevant source and distinct
claim. It must count explicit warrants, lexical fallbacks, unresolved claims,
claimless sources, corrected/superseded/retracted sources, and coverage limits.
Complete claim enumeration is not complete semantic resolution and neither is
evidence of exhaustive search.

### 6. Rebase the hypothesis portfolio

For every live hypothesis assign a literature relation: `apparently_open`,
`partly_anticipated`, `known_special_case`, `absorbed`, `contradicted`,
`independent`, `cross_field_bridge`, or `coverage_unknown`. Record the specific
source IDs and conceptual change. Lack of a match is not proof of novelty.

Preserve high-risk seeds during their generative-license phase, but require this
rebase before active investment, comparison, proof routing, or novelty claims.

### 7. Emit theory and scheduling events

Produce ledger-ready events for changed concepts, assumptions, mechanisms,
genealogy edges, barriers, open questions, retired duplicates, revived routes,
and literature-generated conceptual corners. State which branches can continue,
must reframe, need targeted reading, or are stale.

If a newer snapshot appears during parallel work, do not silently swap it in.
Mark the portfolio `literature_superseded` and rebase all surviving branches
before synthesis or promotion.

## Freshness Policy

Require a current validated snapshot before each major portfolio opening and
before novelty or contribution claims. Freshness is target- and claim-sensitive,
not a fixed number of days. A bounded speculative cycle may proceed with stale
literature only as `literature_blind_incubation`; it cannot claim novelty or win
active investment until rebased.

## Guardrails

- Do not treat the newest paper as the strongest source.
- Do not treat a generated-at timestamp as evidence of a search.
- Do not use one target's `latest` report for another target.
- Do not let literature consensus prohibit a well-typed high-risk hypothesis;
  record the departure and why it may be fruitful.
- Do not launder a missing search into an apparently open gap.
- Do not count duplicated search lanes, citation volume, or provider breadth as
  conceptual coverage.
- Do not describe a lexical relation as semantic understanding or let an old
  source-version warrant survive correction or supersession.

## Mathematical Invariants

Preserve target identity, theorem or phenomenon statement, source claim and
limitation, quantifier and regime scope, conceptual-system IDs, prior theory
state, and snapshot digest. Name the mathematical objects, definitions, and
carriers compared whenever a source-to-theory mapping depends on them. A source
may change plausibility or genealogy without proving or refuting the target
claim. Treat mismatched quantifiers or boundary regimes as explicit edge cases,
not approximate agreement.

## Output Contract

Return one `literature_assimilation_packet` using the reference contract. It
must include snapshot resolution, freshness and coverage, source delta,
the semantic-claim-layer digest and coverage audit, claim-to-theory mappings,
concept and hypothesis updates, opportunity frontier, stale branches, ledger
events, explicit unknowns, and next theory actions.
`selected_snapshot` may be null only for `refresh_required`, and provisional
local mappings must remain distinguishable from a completed rebase.

## Epistemic Discipline

Record epistemic status independently for each source record, interpretive
mapping, hypothesis relation, and theory event. Never inherit status merely
because two records share a citation.

Separate `source_verified`, `search_current`, `coverage_bounded`,
`interpretive_mapping`, `literature_collision`, `apparent_gap`, and
`established_result`. Cite source IDs and exact snapshot identity for every
mapping. Mark inference and novelty boundaries explicitly.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md`. Inspect target-scoped search and
literature artifacts before interpretation, validate their target and digest,
and never claim a live search from a static local packet. Execute collection or
validation commands only when their prerequisites and network authority exist.

## Failure/Demotion

Fail assimilation on target mismatch, missing search provenance, invalid digest,
unresolved global `latest` identity, fabricated coverage, or sources without
claim-level mappings. Demote an apparently novel hypothesis when a source
absorbs it, but preserve any explicit conceptual difference.

## Validation Handoff

End with the frozen snapshot ID, theory-state version, stale or rebased branch
IDs, required targeted searches, and the exact ledger events the single-writer
reducer should consider.
