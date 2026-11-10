<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Inference Quality Criteria

This guide defines the correctness bar for P vs NP discovery claims before they can enter the proof queue, reports, or paper-facing narratives.

## Core Rule

Every nontrivial claim must be represented as a typed inference:

- source statement
- target statement
- inference rule
- model context
- quantifier context
- parameter map
- side conditions
- barrier status
- derivation status
- reviewer decision

A claim is not promoted because it is plausible, fluent, or strategically attractive. It is promoted only when the inference preserves the target object, model, quantifiers, reduction direction, advice status, and proof obligations.

## Required Skills

- [`pvsnp-inference-quality-controller`](../../../skills/orchestration/pvsnp-inference-quality-controller/SKILL.md): central gate for typing and routing claims.
- [`pvsnp-proof-derivation-builder`](../../../skills/reasoning/pvsnp-proof-derivation-builder/SKILL.md): derives theorem-shaped claims and localizes proof debt.
- [`pvsnp-reduction-consistency-reviewer`](../../../skills/evaluation/pvsnp-reduction-consistency-reviewer/SKILL.md): checks transfer direction and parameter maps.
- [`pvsnp-quantifier-uniformity-reviewer`](../../../skills/evaluation/pvsnp-quantifier-uniformity-reviewer/SKILL.md): checks all-length, all-exponent, uniformity, and advice discipline.
- [`pvsnp-barrier-specificity-reviewer`](../../../skills/evaluation/pvsnp-barrier-specificity-reviewer/SKILL.md): prevents generic barrier slogans.
- [`pvsnp-proof-complexity-transfer-reviewer`](../../../skills/evaluation/pvsnp-proof-complexity-transfer-reviewer/SKILL.md): checks proof-system-to-language or circuit transfer.
- [`pvsnp-meta-complexity-carrier-reviewer`](../../../skills/evaluation/pvsnp-meta-complexity-carrier-reviewer/SKILL.md): checks MCSP, MKtP, truth-table, and row-hardness carriers.

## Reduction And Transfer Correctness

The branch must state the source object, target object, reduction type, direction, length map, and transfer inequality.

Valid progress: deriving a statement such as:

`If SAT has SIZE(n^c) circuits, then the source carrier has circuits of size N^{q + beta c + o(1)} under the stated interface.`

Invalid promotion: claiming source-carrier hardness directly implies SAT hardness without proving the reverse transfer or contrapositive.

## Quantifier And Uniformity Correctness

The branch must preserve:

- all lengths versus infinitely often
- all exponents versus fixed exponent
- uniform algorithms versus circuit families
- advice-free versus advice-bearing selection
- total languages versus promise domains
- unrestricted circuits versus restricted circuit classes

Invalid promotion: proving `SIZE(n^3)` lower bounds on infinitely many lengths and claiming `NP not subset P/poly`.

## Barrier Specificity

Barrier language must be branch-specific.

For natural proofs, the branch must check largeness, constructivity, and usefulness against the exact circuit class. For relativization and algebrization, the branch must identify which proof step relativizes or algebrizes. For black-box barriers, the branch must state the interface and escape conditions.

Invalid promotion: saying "natural proofs applies" without checking the property.

## Proof Derivation Correctness

Theorem-shaped claims must include:

- theorem statement
- definitions
- assumptions
- lemma chain
- proof steps
- where each assumption is used
- counterexample or failure regimes
- exact blocked lemma if incomplete

The derivation may end as a conditional theorem or named proof obligation, but it may not be presented as a proof if an essential transfer lemma is missing.

## Proof-Complexity Transfer Correctness

Proof lower bounds are not automatically language or circuit lower bounds. A branch must state the proof system, tautology family, semantic target, simulation direction, and bridge theorem.

Invalid promotion: treating a resolution lower bound as a SAT circuit lower bound.

## Meta-Complexity Carrier Correctness

For MCSP, MKtP, truth-table, row-hardness, or Kolmogorov-style carriers, the branch must state:

- carrier object
- table length and input length
- density regime
- verifier overhead
- row or instance selection rule
- advice status
- transfer certificate to the target class

Invalid promotion: using a nonuniform hard-row selector as if it gives an advice-free NP language lower bound.

## Deterministic Validation

Inference-quality packets are validated by:

```bash
python agentic/scripts/validate_pvsnp_inference_quality.py
```

The repo-wide proof gate also invokes this validator through:

```bash
python agentic/scripts/agentic_check.py
```

The validator checks packet shape and hard invariants. It does not prove the mathematics; it prevents structurally invalid inference claims from entering the promoted workflow state.
