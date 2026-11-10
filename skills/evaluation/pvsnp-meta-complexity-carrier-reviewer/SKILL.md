---
name: pvsnp-meta-complexity-carrier-reviewer
description: Review P vs NP meta-complexity carrier claims involving MCSP, MKtP, truth tables, Kolmogorov-style measures, row-hardness, compression, density, and verifier overhead. Use when a branch risks confusing aggregate or advice-selected hardness with uniform target-language hardness.
---

# P vs NP Meta-Complexity Carrier Reviewer

## Conceptual Role

Use this reviewer when the active branch uses a meta-complexity carrier such as MCSP, MKtP, truth-table hardness, row selection, or compression obstruction. It asks whether the carrier actually transfers to the target separation or only diagnoses a hard-looking proxy.

## Workflow

1. Name the carrier: MCSP, MKtP, truth table family, row-hard certificate, compression map, or ranked witness.
2. State table length, input length, density, verifier overhead, and selection rule.
3. Check whether row or instance selection is uniform and advice-free.
4. Check whether the carrier lower bound transfers to SAT, NP, P/poly, or a restricted circuit class.
5. Identify naturalness, density, constructivity, and barrier status.
6. Decide whether to promote, repair, use as no-go evidence, or quarantine.

## Mathematical Invariants

Mathematical object: carrier, table length, row selection rule, verifier, density regime, source lower bound, target class, and transfer certificate.

Preserved invariants: uniform selection, advice accounting, length mapping, verifier overhead, density, and source-to-target transfer.

Broken invariants: advice-selected rows treated as uniform language hardness, aggregate hardness treated as SAT lower bound, verifier overhead ignored, sparse valid lengths hidden, or density/naturalness left unspecified.

Edge case or counterexample: a nonuniform selector can pick hard rows from an easy aggregate object; this does not yield an advice-free language lower bound.

## Epistemic Discipline

Assign epistemic status: `carrier_typed`, `transfer_certificate_present`, `advice_leak`, `density_gap`, `verifier_overhead_gap`, `naturalness_pressure`, `bounded_proxy_only`, `repair_required`, or `invalid_transfer`.

Cite evidence from MCSP/MKtP definitions, branch IDs, symbolic-auditor outputs, theorem references, cycle IDs, or explicit unknowns.

## Output Contract

Return:

1. `Carrier`: exact meta-complexity object.
2. `Parameter Ledger`: table length, input length, density, verifier overhead, and selection rule.
3. `Uniformity And Advice Audit`: whether selection and verification are advice-free.
4. `Transfer Certificate`: what connects carrier hardness to the target.
5. `Barrier And Naturalness Audit`: largeness, constructivity, usefulness, oracle/algebraic status.
6. `Verdict`: promote, repair, no-go candidate, bounded proxy, or quarantine.
7. `Validation Handoff`: symbolic auditor, reduction reviewer, quantifier reviewer, or derivation builder.

## Failure/Demotion

Demote if the branch cannot name its carrier, selection rule, verifier overhead, density, and target transfer. Quarantine repeated MCSP/MKtP claims that rely on hidden advice or only produce proxy hardness.
