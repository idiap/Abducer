---
name: ym-prove-rg-to-rigidity
description: Domain-private cohere-fast YM procedure to connect renormalization-group bounds to rigidity. Use only with a validated cohere-fast ym activation receipt.
---

# Prove Rg To Rigidity

## Activation boundary

Run only when the request carries a validated `cohere_fast` activation receipt bound to domain `ym`. Never activate from generic Yang--Mills prose and never modify `skills/yang_mills`.

## Contract

- Owner: `cohere_fast/ym`; runtime mode: `domain_private_adapter`.
- Input: a validated `DomainEvidencePacket` plus the step's declared prerequisites and immutable source locators.
- Output: a `DomainEvidencePacket` containing claims, assumptions, derivation or action, counterchecks, open obligations, provenance digests, and a conservative status.
- Claim ceiling: `candidate`; only an independent-audit gate may return `independently_supported`, and no workflow event implies proof.
- Budget: one bounded step, at most 12 primary claims and 20 cited locators; split larger work.

## Procedure

1. Verify workflow, domain, run, parent-event, schema-version, and input digests.
2. Connect renormalization-group bounds to rigidity; state every convention and dependency.
3. Record attempted falsifiers, failed routes, conditional branches, and unresolved obligations.
4. Emit the typed packet without raising its incoming claim ceiling.

## Stop and trace rules

Stop and quarantine on missing provenance, domain mismatch, invalid schema, unbound prerequisite, or contradictory accepted evidence. The public trace must expose premises, evidence locators, warrant, alternatives, uncertainty, ceiling, gate result, and disposition; it must not expose hidden chain-of-thought.
