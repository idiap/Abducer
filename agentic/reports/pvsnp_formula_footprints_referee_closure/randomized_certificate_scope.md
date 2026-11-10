<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Randomized Certificate Scope

- Status: `implemented`
- Decision: `bounded_error_union_proved_expected_variants_open`

## Bounded-Error Model

A randomized verifier receives oracle access to a labeling \(y\) and randomness
\(r\).  For a hard labeling \(y^\star\), completeness requires
\[
  \Pr_r[V^{y^\star}(r)=1]\ge 2/3.
\]
For every easy completion \(y\) whose induced source function has circuit size
at most \(s\), soundness requires
\[
  \Pr_r[V^y(r)=1]\le 1/3.
\]

The deterministic certificate theorem applies only to fixed accepted
transcripts under perfect soundness.  With bounded error, an accepted transcript
on one random seed need not reject all easy completions.  Therefore the
deterministic completion argument does not automatically transfer.

## Candidate Resource Measures

| Measure | Meaning | Status |
|---|---|---|
| Expected footprint | Expected number of queried labels over verifier randomness. | Needs distributional lower bound. |
| Accepting-query union footprint | Number of labels queried on accepting executions. | Proved: if hard-label acceptance exceeds easy-completion soundness, the accepting-query union is a deterministic certificate. |
| Information revealed | Mutual information between transcript and hard labeling. | Plausible but requires information-theoretic proof. |
| Communication-query product | Product of proof/message length and query count. | Relevant to interactive protocols, not in current draft. |
| Transcript support size | Number of distinct accepted query transcripts. | Requires minimax or corruption-style argument. |

## Required Theorem Shape

A stronger randomized extension should prove one of:

\[
  \mathbb E_r[|\mathrm{Footprint}(r)|]\ge \widetilde{\Omega}(s),
\]
or
\[
  I(y^\star;\mathrm{Transcript})\ge \Omega(s),
\]
or a comparable bound under an explicitly stated distribution over hard and
easy completions.

## Decision

The current paper claims only the bounded-error accepting-query union theorem.
Expected footprint, transcript support, minimax, and information-theoretic
variants remain open unless a separate distributional argument is added.

## Paper Text To Add

> Bounded-error verifiers inherit the deterministic footprint lower bound for
> the union of labels queried on accepting executions whenever hard-label
> acceptance exceeds the soundness bound for easy completions.  Expected-query
> and information-theoretic lower bounds are not claimed.
