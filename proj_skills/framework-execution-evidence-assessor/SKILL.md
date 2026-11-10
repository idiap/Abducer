---
name: framework-execution-evidence-assessor
description: Assess repository execution and test receipts for framework-paper claims. Use when Codex must distinguish observed, replayed, verified, missing, and contested runtime evidence without inferring frequency, effectiveness, cost, generalization, or end-to-end reachability from code, documentation, Git history, or test existence alone.
---

# Framework Execution Evidence Assessor

Consume only indexed evidence records and named receipt candidates.

1. Identify the exact subject, invocation, inputs, environment, outcome, and immutable receipt.
2. Use `observed` for a recorded run, `replayed` for an independently repeated eligible run, and `verified` only for a named validator's bounded conclusion.
3. Use `missing` when no eligible receipt exists and `contested` when authorities conflict.
4. Record limitations for scope, freshness, replication, and environment.
5. Validate `ExecutionEvidenceModel` and bind it to the evidence-index digest.

Never execute discovered code during assessment. Tests demonstrate only their asserted scope. Compilation demonstrates syntax/build status, not scientific validity. Hand explicit evidence nulls and contested states forward rather than omitting them.
