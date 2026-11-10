---
name: pvsnp-conceptual-pressure-localizer
description: "Localize the conceptual pressures that make a P vs NP branch hard. Use when a P vs NP marathon, report, queue item, proof route, contradiction route, or paper-facing subgoal needs to explain the essential bottleneck before proposing another analysis: verification-versus-search, source-to-target transfer, quantifier order, uniform/nonuniform model choice, relativization, natural proofs, algebrization, advice leakage, padding/projection debt, or meta-complexity carrier pressure."
---

# P vs NP Conceptual Pressure Localizer

## Conceptual Role

Use this skill at the beginning of a P vs NP reasoning slice. Its job is to locate why the branch is hard in complexity-theoretic terms before the loop spends budget on proof search. It turns vague difficulty language into typed pressure: what object would have to be lower-bounded, what transfer would have to preserve the target, which barrier applies, and where proof debt is being moved.

This is a generative interpretation skill. Do not only list known barriers. Interpret the active artifact, infer the branch's hidden burden, and state what would count as real progress.

## Workflow

1. **Name the target and branch.**
   State whether the branch aims at `P != NP`, `NP not subset P/poly`, SAT circuit lower bounds, a meta-complexity carrier, a padding/projection route, or a no-go theorem about one of these.

2. **Localize the pressure source.**
   Classify each pressure as one or more of:
   `verification_search_gap`, `uniform_nonuniform_gap`, `source_target_transfer_gap`, `quantifier_strength_gap`, `barrier_pressure`, `density_naturalness_pressure`, `advice_leakage`, `padding_projection_debt`, `meta_complexity_carrier_debt`, `diagonalization_boundary`, or `proof_debt_relocation`.

3. **State why it is essentially hard.**
   Explain the hardness in the branch's own objects. For example, do not say only "natural proofs applies"; say whether the proposed property is large, constructive, useful against the target circuit class, and whether pseudorandom-function barriers would make the route self-defeating.

4. **Preserve model and quantifier discipline.**
   Record the model (`P`, `NP`, `P/poly`, `SIZE(n^c)`, oracle, algebraic, promise, average-case, meta-complexity carrier), quantifier order, input-length map, and uniformity assumptions. Identify any hidden switch of model as a broken invariant.

5. **Separate route value from target proof.**
   Decide whether the branch can deliver a main-target advance, a publishable obstruction/no-go theorem, a diagnostic lemma, or only a restatement of known difficulty.

6. **Emit next controls.**
   Give content-specific `persist/adapt/backtrack/pivot/quarantine` conditions. A branch should persist only if the next step computes a transfer, proves an obstruction, or narrows a barrier in the same model.

## Mathematical Invariants

- Mathematical object: target statement, source carrier or language, target class, reduction or transfer theorem, circuit model, barrier regime, quantifier pattern, and validation handoff.
- Preserved invariants: same target separation, same complexity model, same input-length regime, same source lower-bound class, same quantifier strength, and explicit barrier status.
- Broken invariants: replacing `P != NP` with a proxy lower bound without transfer, proving only bounded-exponent lower bounds while claiming all-polynomial separation, moving to sparse valid lengths without a certificate, importing an oracle or algebraic result as unrelativized evidence, or hiding advice/nonuniformity.
- Edge case or counterexample: a branch that proves hardness only for fixed exponent `c`, fixed padding parameter `k`, sparse valid lengths, promise inputs, or a natural large property may be valuable but cannot be promoted as target progress without a transfer certificate.

## Epistemic Discipline

Assign epistemic status to each pressure and route: `localized`, `partially_localized`, `proof-obligation`, `barrier-backed`, `diagnostic-only`, `contribution-shaped`, `blocked`, `refuted`, `promoted`, `quarantined`, or `explicit_unknown`.

Cite KB IDs, cycle IDs, queue item IDs, timeline report sections, source artifacts, prior-art references, validator output, or explicit unknowns for every substantive pressure claim. Treat "this is hard" as unsupported unless the exact object, transfer, model, or barrier is named.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the pressure map. Useful deterministic runs include report validation, queue extraction, skill-dispatch summaries, or KB parsing. Inspect generated artifacts before interpreting them; artifact existence is not mathematical progress.

## Output Contract

Return:

1. `Target And Branch`: target claim, branch label, source artifact, and current proof posture.
2. `Conceptual Pressure Map`: typed pressures, witnesses, why each pressure is hard, and which object carries it.
3. `Barrier And Model Audit`: relativization, natural-proofs, algebrization, nonuniformity/advice, diagonalization, and meta-complexity status for this branch.
4. `Debt Relocation Check`: whether the route reduces the problem or merely moves the difficulty to sparse lengths, stronger source lower bounds, naturalness, advice, or uniformity.
5. `Progress Criterion`: exact theorem, computation, transfer inequality, contradiction, or no-go lemma that would count as progress.
6. `Branch Control`: content-specific persist, adapt, backtrack, pivot, quarantine, and stop conditions.
7. `Validation Handoff`: next skill, validator, report section, queue item, or proof obligation that should control the loop.

## Failure/Demotion

Demote when the output only recites famous barriers, cannot name source and target objects in the same model, ignores quantifiers, lacks evidence citation, or confuses a diagnostic obstruction with proof of `P != NP`. Quarantine a branch if two sharpened attempts still cannot state a target-preserving transfer or formal no-go theorem.

## Validation Handoff

Hand localized pressures to `pvsnp-qualitative-complexity-reasoner` when relation variables or transfer exponents need typing, to `pvsnp-impossibility-theorem-forger` when the best next contribution is a no-go theorem, and to `next-experiment-queue-ranker` when the branch needs priority ordering. Use `agentic/scripts/validate_discovery_marathon_report.py` after report-facing changes.
