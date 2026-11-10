
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Governance Criteria

## Purpose

This reference prevents discovery from collapsing into uncontrolled depth-first search.
Its job is to decide when a route has earned deeper work, when the search must broaden, and when a partial result is already strong enough to count as a major contribution.

## Part I: Anti-Drift Rules

Depth is justified only if at least one of the following changed in the last cycle:

1. a previously schematic bridge object became typed;
2. a theorem-body-grounded claim replaced a schema label;
3. a new route-specific lemma became stateable;
4. the negative route or barrier diagnosis became sharper;
5. the same carrier now works across a harder model or threshold regime;
6. the route compressed multiple nearby branches into one object or principle.

If none of these changed, depth is not progress.

### Drift Signals

Mark a route as drifting when two or more hold:

- the carrier remains a placeholder after repeated passes;
- the same branch is revisited without a new theorem-pair-specific lemma;
- obligations are being decomposed into more obligations without stronger statements;
- proof sketches rename the bridge object rather than clarify it;
- search history shows repeated refinement within one branch while neighboring high-value branches stay untouched.

### Governance Decisions

- `deepen`:
  only if the route gained new typed structure or sharpened theorem content.
- `lateralize`:
  when the route is informative but no longer improving fast enough.
- `freeze`:
  when the route currently adds neither theorem content nor search-space compression.
- `queue-for-proof`:
  when the route now supports a self-contained claim under test.
- `major-subresult-candidate`:
  when the route yields an independently valuable theorem, barrier, tool, or transfer principle.

## Part II: What Counts As a Major Subresult

A subresult is major only if it passes all mandatory gates:

1. self-contained statement:
   it can be stated without referring to the unfinished global program.
2. mathematical inspectability:
   an expert can inspect the statement, assumptions, and proof idea directly.
3. nontrivial frontier relation:
   it shifts, sharpens, or organizes a real mathematical frontier.
4. independent value:
   it would matter even if the main conjecture stayed open.

If any gate fails, the subresult is exploratory, not major.

### Major Subresult Types

#### A. Standalone Theorem

Counts as major when it does at least one:

- proves a new lower bound, separation, transfer theorem, or structural theorem;
- makes a previously schematic bridge theorem precise;
- resolves a substantial intermediate theorem on the main route.

#### B. Barrier or Impossibility Result

Counts as major when it does at least one:

- rules out an entire family of bridge objects or transport mechanisms;
- proves that a commonly attempted route cannot work under explicit assumptions;
- converts diffuse failure into a theorem-level obstruction.

#### C. Bridge Object or Tool

Counts as major when it does at least one:

- introduces a typed object that unifies several nearby routes;
- exposes a new invariant with clear transport and payoff roles;
- yields a reusable surrogate problem, certificate, or dual object with independent applications.

#### D. Transfer Principle

Counts as major when it does at least one:

- shows a repeatable movement across models, thresholds, or formulations;
- explains why several formerly separate bridge attempts are instances of one mechanism.

## Part III: Major Contribution Score

Score each subresult on a 0-3 scale for each axis:

1. `frontier_shift`
- 0: no clear frontier effect
- 1: local clarification only
- 2: sharpens a real open route or known barrier
- 3: creates a clear theorem-level shift or closes a meaningful route family

2. `independence`
- 0: only meaningful inside the current run
- 1: useful mainly as internal scaffolding
- 2: meaningful to experts on the problem even without the final goal
- 3: clearly publishable as an independent result

3. `transferability`
- 0: one-route artifact only
- 1: maybe relevant to one neighboring route
- 2: applies across multiple nearby routes
- 3: defines a reusable principle or object family

4. `barrier_clarity`
- 0: failure remains vague
- 1: exposes a local weakness
- 2: sharpens a meaningful obstruction
- 3: yields a theorem-like impossibility or strong negative frontier

5. `proof_closure`
- 0: still mostly aspirational
- 1: statement exists but proof architecture is weak
- 2: proof or refutation plan is explicit and inspectable
- 3: proof, refutation, or reduction is essentially closed modulo standard verification

6. `search_compression`
- 0: no reduction in search uncertainty
- 1: narrows one branch
- 2: eliminates or unifies several branches
- 3: reorganizes the search space in a simpler and more powerful way

### Threshold

Treat a subresult as a major contribution candidate only if:

- all mandatory gates pass; and
- `frontier_shift + independence + transferability + barrier_clarity + proof_closure + search_compression >= 11`; and
- at least one of `frontier_shift`, `independence`, or `barrier_clarity` is `3`.

This prevents inflated scores from coming only from internal neatness.

