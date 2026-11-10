---
name: framework-paper-claim-curator
description: Create and enforce a typed claim ledger for an AI framework paper. Use when Codex must bind exact claims to evidence, counterevidence, assumptions, limitations, freshness, allowed rhetorical verbs, section ownership, external-citation requirements, and named execution receipts before any section writer is allowed to produce prose.
---

# Framework Paper Claim Curator

Consume the frozen evidence index and validated functional, workflow, execution, and abstraction models.

1. Assign each claim a class: `descriptive`, `interpretive`, `evaluative`, `comparative`, `novelty`, or `proposed`.
2. Assign an independent status: `declared`, `observed`, `replayed`, `inferred`, `verified`, `unknown`, or `contested`. Never treat this set as one confidence ladder.
3. Record exact scope, evidence and counterevidence IDs, assumptions, limitations, freshness, allowed verbs, and allowed sections.
4. Require external literature for comparative or novelty claims.
5. Require named receipts for observed, replayed, or verified evaluative claims.
6. Withhold stale, unknown, or unresolved contested claims from assertive prose.
7. Validate `PaperClaimLedger` and bind it to all input digests.

Reject efficacy from topology, proof claims from workflow correctness, novelty from local absence, and stronger wording than the ledger permits. Hand writers only their allocated claim IDs and required caveats, never unrestricted repository files.
