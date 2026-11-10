---
name: failed-hypothesis-anticipator
description: Run a prompt-based premortem for proof hypotheses and proof pathways before investing major cycle budget. Use when a discovery marathon, Yang-Mills workflow, mathematical-physics branch, P vs NP route, result-atlas candidate, or publication-consolidation subgoal must anticipate likely failure modes, shallow/incremental drift, missing artifacts, proxy shifts, hidden transfer assumptions, low physics reward, or non-publication-worthy hypotheses before proof-search cycles continue.
---

# Failed Hypothesis Anticipator

## Purpose

Anticipate failed hypotheses declaratively before spending cycle budget. The
skill does not reject difficult work merely because it is difficult. It asks
whether the proposed route has identifiable failure signatures that should be
tested, reframed, or quarantined before ordinary proof search.

## Mathematical Invariants

Bind the mathematical object before the premortem: source object, target object, carrier, model/theory, transfer interface, quantifiers, validity regime, and intended route decision. A failure anticipation is valid only if it preserves those invariants while asking how the route could fail.

Required edge cases and counterexamples include proxy shifts, finite-to-global gaps, noncommuting limits, missing uniformity, hidden target-equivalent assumptions, prior-art collisions, and artifact debt that would make the hypothesis only definitionally true.

## Epistemic Discipline

Every anticipated failure must carry an epistemic status, evidence citation, source artifacts, explicit unknowns, and validation handoff. Label the route as `invest`, `artifact_sprint`, `falsifier_sprint`, `reframe`, `demote`, `quarantine`, or `stop` with a reason tied to evidence, not mood.

Disconfirming evidence or absent falsifiers should change the route state before another ordinary cycle starts. Do not let an attractive high-level idea continue if its next test cannot fail or cannot plausibly support a major publication path.

## Premortem Questions

For each hypothesis or pathway, answer:

1. What is the smallest claim that would count as success?
2. Which source object, target object, carrier, and transfer interface are
   independently meaningful?
3. Which exact artifact or theorem must exist before the route can move?
4. Which hidden assumption would make the claim tautological, definitional, or
   proxy-like?
5. Which physical, mathematical, or complexity-theoretic gate would fail first?
6. What is the quickest falsifier, negative example, sign test, model check, or
   literature disqualifier?
7. What would make this route a major publication path rather than an
   incremental lemma?

## Declarative Heuristics

Flag a route when any signature is present:

- `missing_carrier`: no physical/computational/mathematical carrier links source
  to target.
- `proxy_shift`: proof object silently changes theory, model, observable, or
  problem.
- `finite_to_global_gap`: finite or local result is treated as continuum,
  asymptotic, global, or Clay-level evidence.
- `uniformity_gap`: a bound is useful only at fixed cutoff, size, source, or
  parameter.
- `definitional_transfer`: the target property is defined as the bridge image.
- `artifact_debt`: promotion depends on a named table, interval, code output,
  literature theorem, or proof object that does not exist.
- `no_falsifier`: the next cycle cannot fail in a way that changes route state.
- `low_publication_reward`: success would add an appendix lemma but not change
  field understanding.
- `literature_collision`: the claim appears close to known constructive-QFT,
  OS/Wilson, proof-complexity, or barrier machinery without a clear delta.
- `noncommuting_limits`: the route crosses cutoff, volume, time, regulator, or
  asymptotic limits without an order-of-limits ledger.

## Dispositions

Use one of:

- `invest`: high reward and the quickest failure test is explicit.
- `artifact_sprint`: a named artifact decides the route before broad proof
  search.
- `falsifier_sprint`: a cheap negative test decides whether to continue.
- `reframe`: promising idea, wrong or underpowered representation.
- `demote`: support-only, appendix-only, or finite local result.
- `quarantine`: proxy-like, low reward, artifact-missing, or stale repeated
  blocker.
- `stop`: no target link, no falsifier, and no major reward path.

## Output Contract

Return a `failed_hypothesis_anticipation` object with:

- `hypothesis_id`
- `target_id`
- `candidate_claim`
- `premortem_questions`
- `declared_failure_signatures`
- `earliest_decisive_test`
- `artifact_debt`
- `publication_reward_assessment`
- `recommended_disposition`
- `prompt_heuristic_for_next_cycle`
- `validation_handoff`

## Quality Bar

The answer must be actionable before another cycle starts. If the route is
allowed to continue, name the next falsifier or artifact. If it is blocked,
state exactly which hidden assumption, missing object, or low-reward condition
caused the block.

## Failure/Demotion

Demote when the hypothesis lacks a carrier, falsifier, artifact gate, literature gap, or major publication reward. Quarantine when the hypothesis is proxy-like, target-equivalent, low relevance, repeatedly blocked, or only produces incremental support without changing a hard gate.
