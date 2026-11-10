---
name: parallel-hypothesis-portfolio
description: Orchestrate independent high-risk theory branches in parallel from a frozen target, theory-state, and literature snapshot, then validate, compare, cross-pollinate, and merge their learning through a single-writer reducer. Use when several structurally different hypotheses can mature concurrently, when a major discovery cycle needs protected diversity, or when existing marathon parallelism must avoid shared-state corruption, duplicated work, cross-branch anchoring, and all-or-nothing loss.
---

# Parallel Hypothesis Portfolio

## Role

Turn conceptual diversity into safe parallel work. Parallelize independent
theory maturation, not uncontrolled writes. Preserve divergent intuitions long
enough to learn from them, then converge through explicit comparison and one
serialized theory-state commit.

Read [references/parallel-portfolio-contract.md](references/parallel-portfolio-contract.md)
before opening workers.

## Entry Gate

Require a target ID, portfolio ID, base theory-state version and digest, frozen
literature snapshot ID and digest, validated high-risk hypothesis seeds,
pairwise-overlap assessment, per-branch budgets, and a single-writer reducer.

Only independent or read-only tasks may share a wave. Put hypothesis
dependencies in a DAG and delay a child until its inputs commit at a barrier.

## Workflow

### 1. Freeze the common basis

Create an immutable portfolio manifest. Every worker receives the same target
commitments, theory snapshot, literature snapshot, non-claim boundary, and
resource policy. Never resolve a mutable global `latest` inside a worker.

### 2. Design genuinely different lanes

Select branches by conceptual distance, not only score. Prefer complementary
lanes such as conservative deepening, ontology inversion, cross-field transfer,
negative/impossibility theory, new mediator, and unifying synthesis. Deduplicate
branches whose primitives, mechanism, and maturation question are equivalent.

Use `high-risk-hypothesis-forger` for seeds and
`long-horizon-route-portfolio-manager` for target relevance and budget balance.

### 3. Fan out isolated workers

Give each branch a branch-local artifact namespace, immutable input digest,
allowed skills, forbidden cross-branch context, budget, stop condition, and
expected theoretical delta. Workers may not mutate the theory ledger, active
branch files, global reports, or another branch's artifacts.

Reuse the existing marathon `--parallel-branches` and `--api-max-workers`
surface where its execution contract fits. Do not claim that the current API
runner already supplies transactional state, literature rebasing, or partial
success recovery.

### 4. Validate at a barrier

Collect one typed receipt and theory delta per branch. Validate identity,
digests, output contract, target relevance, literature basis, and resource use.
Preserve valid successes even when another worker fails; store failures and
timeouts as branch-local negative knowledge. Invalid packets never enter merge.

### 5. Cross-pollinate deliberately

After the blind divergence wave, optionally run a second read-only wave in which
paired branches steelman, challenge, or hybridize each other. Record ancestry so
a synthesis cannot masquerade as an independent discovery.

### 6. Merge once

The reducer compares validated deltas on relevance, conceptual depth,
understanding, unification, generativity, literature relation, coherence, and
truth-aptness. It commits ancestry, opposition, synthesis, duplication,
contradiction, and next-action events with compare-and-swap against the base
state version.

Do not select by majority vote or one scalar. Retain at least one serious
high-upside dissenter when it remains nondominated.

### 7. Rebase on newer literature

If a new search snapshot completes mid-wave, finish the frozen wave but mark it
`literature_superseded`. Run `frontier-literature-assimilator` on every surviving
branch before synthesis, further budget, proof routing, or novelty claims.

## Parallel Safety Invariants

- frozen target, theory, and literature digests per wave;
- branch-local writes and idempotent invocation IDs;
- no global `latest` reads or writes inside workers;
- one validated receipt per attempt;
- single-writer compare-and-swap merge;
- partial success preservation;
- deterministic scheduler-order rendering without equating order with merit;
- explicit resource and cancellation status.

## Guardrails

- Do not parallelize dependent theory steps in the same wave.
- Do not give every worker the same prompt under different branch names.
- Do not allow early cross-talk to collapse intuitive diversity.
- Do not discard valid branches because one sibling failed.
- Do not merge stale literature assumptions silently.
- Do not mistake more workers for more conceptual coverage.

## Mathematical Invariants

Preserve target commitments, conceptual-system ancestry, hypothesis identity,
quantifier and regime scope, protected successes, snapshot digests, and the
meaning of every branch-local claim. A synthesis must name what it preserves,
changes, and loses from each parent.

## Output Contract

Return the portfolio manifest, wave plan, branch requests and receipts,
validation barrier, partial-failure ledger, diversity and overlap matrix,
cross-pollination results, merge proposal, reducer receipt, retained dissent,
and next parallel or serial actions defined in the reference contract.

## Epistemic Discipline

Record epistemic status per attempt and per theory delta; do not promote a
branch because its execution status is successful.

Separate branch completion, artifact validity, conceptual learning, literature
currency, theory preference, model support, and truth status. Failed execution
is not refutation; majority agreement is not evidence; independent convergence
is meaningful only when branches did not share the decisive inference.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md`. Inspect the manifest and all worker
receipts before merge. Run only bounded, authorized workers. Capture exact
commands or invocation metadata, and state when this skill is producing a plan
rather than executing a runtime.

## Failure/Demotion

Invalidate a wave on mutable shared inputs, target or digest mismatch,
cross-branch writes, missing receipts, duplicate branch disguises, or an
unserialized merge. Preserve independently valid packets and explicitly rebase
rather than erasing them.

## Validation Handoff

End with validated and failed branch IDs, frozen and newest literature snapshot
IDs, reducer state version, retained wildcards, unresolved conflicts, resource
usage, and the next dependency-ready wave.
