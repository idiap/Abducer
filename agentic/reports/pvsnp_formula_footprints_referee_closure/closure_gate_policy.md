<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Closure Gate Policy

- Status: `implemented`
- Applies to: Formula Footprints and Full Rows branch.
- Rule: no new open-ended P vs NP marathon output may promote this draft unless it closes, invalidates, demotes, or quarantines an objection-ledger item.

## Required Fields For New Result Cards

Every result card touching this draft must include:

- `external_anchor`: nearest literature object and novelty delta.
- `nonvacuity_witness`: explicit example, rank condition, counting existence, or conditional status.
- `sharpness_status`: matching bound, separation, necessary-condition only, or unknown.
- `demotion_boundary`: what the claim becomes if the missing theorem is not supplied.
- `paper_claim_status`: proved, patched, supporting lemma, conditional calibration, not claimed, or future work.
- `closed_objection_ids`: objection ledger IDs closed or updated.

## Promotion States

| State | Meaning |
|---|---|
| `proved` | Definitions, theorem, and proof close the relevant objection without new hidden assumptions. |
| `patched` | A technical issue is repaired without changing asymptotics or theorem scope. |
| `supporting_lemma` | Correct but not central enough for the paper claim. |
| `conditional_calibration` | Useful under a named hypothesis, but not evidence for that hypothesis. |
| `demoted` | Removed from main contribution status. |
| `future_work_quarantine` | Named open problem; cannot be used in the paper claim. |
| `invalidated` | Claim or route is wrong or circular. |

## Blocking Rule

A result is blocked from paper promotion if any of the following fields are
missing:

1. `external_anchor`
2. `nonvacuity_witness`
3. `sharpness_status`
4. `demotion_boundary`
5. `paper_claim_status`
6. at least one `closed_objection_ids` value or a new objection ID

## Default Demotions

- Row-forcing results default to `supporting_lemma`.
- Quotient-distance results default to `supporting_lemma`.
- SAT magnification results default to `conditional_calibration`.
- Standard proof-system lower-bound language defaults to `not_claimed`.
- Restricted proof-system bridge language defaults to `proved_only_when_a_matching_normalizer_packet_exists`.
- Bounded-error accepting-union language defaults to `proved_union_only`.
- Expected-query or information-theoretic randomized language defaults to `future_work_quarantine`.

## Closure Definition

- `closed`: the artifact satisfies the objection's close condition.
- `partly_closed`: the artifact supplies examples or demotions but leaves a named mathematical theorem open.
- `demoted`: the claim remains true or useful but no longer supports the advertised paper contribution.
- `quarantined`: the topic is moved to future work and cannot be used as support.
- `invalidated`: the claim should be removed or replaced.
