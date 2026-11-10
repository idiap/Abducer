
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Conjecture Value Rubric

## Purpose

This rubric scores the value of a conjecture as a research object.
It is not a truth score.
It answers: if this conjecture were pursued, how much mathematical value would be at stake?

## Mandatory Preconditions

Do not score a conjecture as high-value unless it has:

1. a self-contained statement;
2. a typed carrier, invariant, or mechanism if it introduces an object;
3. a theorem-pair or frontier context;
4. a clear positive and negative test path.

Without these, the conjecture is too vague to govern discovery.

## Axes

Score each axis from 0 to 4.

### 1. Specificity

- 0: topic label only
- 1: partial statement with key terms still schematic
- 2: clear claim but missing typed mechanism or regime control
- 3: theorem-pair-specific and typed
- 4: theorem-pair-specific, typed, and equipped with admissibility conditions

### 2. Consequence Leverage

- 0: little downstream consequence
- 1: minor local clarification
- 2: affects one substantial route
- 3: materially strengthens the main route or a neighboring frontier
- 4: would imply a major separation, major barrier, or major transfer principle

### 3. Independent Subresult Potential

- 0: worthless without the main conjecture
- 1: useful only as internal scaffolding
- 2: could yield a modest standalone lemma
- 3: likely yields an independently interesting theorem, tool, or barrier result
- 4: strong standalone contribution even if the main problem remains open

### 4. Cross-Route Leverage

- 0: isolated branch
- 1: relevant to one neighboring branch
- 2: touches several nearby branches
- 3: coordinates multiple routes through one common object or principle
- 4: reorganizes a significant portion of the search space

### 5. Falsifiability

- 0: no meaningful disconfirmation path
- 1: only vague failure language
- 2: at least one route-specific negative test
- 3: clear positive and negative routes with discriminative value
- 4: failure would itself prove or strongly support a major obstruction

### 6. Barrier Exposure

- 0: disconnected from known barriers
- 1: barrier discussion is cosmetic
- 2: conjecture interacts with a known barrier family
- 3: conjecture either escapes or sharpens a real barrier frontier
- 4: conjecture is central to deciding whether an entire route family survives

### 7. Search-Space Compression

- 0: does not simplify search
- 1: narrows one proof obligation
- 2: removes several low-value variants
- 3: identifies the central bottleneck explicitly
- 4: collapses many speculative branches into a small set of decisive questions

### 8. Tractability

- 0: no visible route toward inspection
- 1: only abstract aspiration
- 2: explicit obligations but weak proof traction
- 3: clear proof or refutation agenda
- 4: close to queue-ready proof work

## Value Score

Use:

`value = 0.16*specificity + 0.18*consequence_leverage + 0.16*independent_subresult_potential + 0.12*cross_route_leverage + 0.12*falsifiability + 0.10*barrier_exposure + 0.10*search_space_compression + 0.06*tractability`

on normalized 0-1 axis values.

## Interpretation

- `>= 0.80`: high-value conjecture
  pursue aggressively or queue for proof
- `0.65 - 0.79`: valuable conjecture
  keep active, but compare against adjacent routes
- `0.45 - 0.64`: exploratory conjecture
  pursue only if it offers special breadth or barrier insight
- `< 0.45`: low current value
  freeze, re-encode, or demote

## Tie-Break Rules

When two conjectures score similarly, prefer the one with:

1. higher independent subresult potential;
2. higher falsifiability;
3. higher search-space compression;
4. lower dependency on untyped bridge objects.

This prevents the system from overvaluing merely elegant but inert conjectures.

