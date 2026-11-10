---
name: proof-same-domain-transfer-certifier
description: Audit whether a proof transfer preserves model, category, regulator, representation, complexity class, semantic regime, and quantifier discipline. Use before accepting transfer-shaped arguments.
---

# Proof Same-Domain Transfer Certifier

Check that a transfer has not quietly changed the problem.

## Critical Conceptual Depth

Same-domain transfer is conceptually deep when it proves that the decisive
structure survives a change of presentation without changing the problem. Ask
whether the argument preserves the actual source of difficulty: positivity,
locality, regulator discipline, quantifiers, uniformity, reduction type,
semantic carrier, or proof-system meaning.

## Value Signal

State what the transfer certificate would make possible. It should let a
result travel to the target theorem without losing meaning, expose why a proxy
was legitimate, or reveal the precise obstruction that prevents travel. If it
only says the same symbol appears in two places, demote it.

## Mathematical Invariants

- Compare mathematical objects, definitions, source and target domains,
  preserved invariants, broken invariants, and boundary regimes.
- Distinguish allowed transformations from domain-changing substitutions.
- Require edge cases or counterexamples where the transfer would fail without
  its certificate.

## Epistemic Discipline

- Cite artifact paths, KB ids, proof packets, prior cycles, and explicit
  unknowns.
- Label transfer status as certified, certificate_needed, support_only,
  blocked, demoted, refuted, or quarantined.
- Do not treat similar notation or heuristic bridges as transfer theorems.

## Output Contract

Return:

- `source_object`
- `target_object`
- `source_domain`
- `target_domain`
- `preserved_structure`
- `changed_structure`
- `transfer_theorem`
- `missing_certificate`
- `same_domain_status`
- `stress_or_failure_case`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote if the transfer changes model, category, regulator, representation,
complexity class, semantic regime, or quantifier discipline without a repair
certificate. Quarantine transfers that hide domain shift behind notation.
