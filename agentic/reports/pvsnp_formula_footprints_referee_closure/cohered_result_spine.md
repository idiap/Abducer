<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Cohered Result Spine

- Status: `implemented`
- Criteria affected: `C11`, `C1`, `C5`, `C10`
- Gate role: operational admission test for new theorem additions.

## Spine

The paper is organized around one flagship result package:

> Completion-sound local evidence for generator-induced hardness must expose a large two-polarity formula footprint; every proof-system or randomized consequence is admitted only insofar as it extracts, charges, sharpens, or bounds this same footprint obstruction.

This is the cohered-results criterion.  The draft should not read as a fragmented ensemble of results or a pile of locally correct but separately motivated payoffs.  Cohered results are a criterion for admission to the main paper, not a retrospective narrative polish.  A locally correct lemma is still rejected if it does not clarify the flagship formula-footprint barrier, its sharpness, its proof-system reach, or its nonclaim boundary.  The required object is one recognizable result arc: a sharp theorem, its calibrations, its controlled interfaces, and its explicit boundaries.

## Result Roles

Every admitted main-paper result must declare one of these roles: flagship, calibration, interface variant, proof-system bridge, or boundary.

| Role | Admitted object | Current examples |
|---|---|---|
| Flagship | The central sharp theorem that carries the paper's identity. | Formula-footprint barrier theorem. |
| Calibration | A result showing that the flagship theorem is nonvacuous, near-tight, or placed at the right scale. | Identity-carrier generic sharpness; SAT parity calibration. |
| Interface variant | A result showing how the same completion-soundness obstruction changes under a different local interface. | Row-forcing theorem; quotient-distance theorem; semantic-relation support certificate; acyclic OR-tree residual certificate; OR-DAG frontier residual certificate; acyclic Boolean frontier residual certificate; visible adaptive frontier residual certificate; visible adaptive branching-program frontier residual certificate. |
| Proof-system bridge | A theorem extracting or charging the same footprint obstruction inside a proof artifact. | Displayed-atom extraction; explicit/support-local resolution; extension normalizers; displayed acyclic ER; compressed and macro-compressed ER tradeoffs; support-declared macro ER budgets; support-audited LRAT trace budgets; provenance-typed LRAT support audits; namespace-typed LRAT antecedent closure; strict-prefix Qrep replay; controller-complete adaptive audit; trace-complete DPLL decision-log normalizer; antecedent-complete CDCL learned-clause normalizer; RUP-complete CDCL support normalizer; canonical-namespace RUP-CDCL standardizer; carrier-independent audit upgrade criterion; self-auditing RUP-CDCL instantiation; append-only self-auditing RUP-CDCL instantiation; prefix-typed append-only RUP-CDCL instantiation. |
| Boundary | A result or remark preventing overclaiming outside the proved model. | No unrestricted Frege, Extended Frege, IPS, arbitrary compressed proof, unaudited or untyped LRAT/DRAT support, delayed quotient-certificate support, hidden adaptive transcript-only support, arbitrary provenance-free CDCL support, public-label syntax as a free auxiliary support-locality certificate, or explicit hard SAT-family claim; prefix-typed RUP support-witness necessity, support-audit necessity, support-erasure, plain LRAT extraction trichotomy, CDCL antecedent-erasure trichotomy, and hidden adaptive transcript insufficiency separators. |

## Admission Rule

A new theorem, corollary, or proof packet may enter the main paper only if its result card answers all five questions:

1. Which role above does it play?
2. Which flagship obstruction does it strengthen: formula footprint, forced rows, quotient distance, randomized accepting union, or proof-object support budget?
3. What is the before/after understanding shift?
4. What nearest-literature or nearest-model boundary does it clarify?
5. What claim remains explicitly unproved after adding it?
6. Why would the result lose force, or become misleadingly motivated, if separated from the flagship theorem arc?

If these answers are weak, the result belongs in a queue, appendix, or future-work note rather than the main theorem package.  The criterion is deliberately asymmetric: coherence can admit a modest supporting lemma, but incoherence rejects even a technically correct result when it fragments the paper's single before/after understanding shift.

## Current Gate Decision

The current package passes C11 at the strong-preprint level because the theorem order now has a visible result arc:

1. flagship formula-footprint lower bound;
2. identity-model sharpness and interface variants;
3. randomized accepting-union robustness;
4. displayed/local/support-normalized proof-system bridges;
5. compressed-proof and hidden-adaptive tradeoffs only when expansion, support accounting, controller completeness, or local equivalence is visible;
6. explicit nonclaim boundaries and a focused next proof obligation.

It is not top-ready because the proof-system bridge is now concrete for enriched self-auditing RUP-CDCL and for the less annotated append-only and prefix-typed subcases, but still needs an externally recognizable system with fewer self-audit fields, and the SAT route is still conditional rather than an explicit hard-family theorem.  The RUP-complete, canonical-namespace, carrier-independent, self-auditing, append-only, and prefix-typed CDCL steps preserve the positive non-plain CDCL route while the support-witness necessity boundary makes the remaining target narrower than a fragmented theorem search: supply an intrinsic support-locality invariant, handle deletion-bearing or untyped traces, or switch to an explicit SAT/source theorem.
