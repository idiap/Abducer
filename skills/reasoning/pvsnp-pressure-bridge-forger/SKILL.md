---
name: pvsnp-pressure-bridge-forger
description: Forge target-preserving bridge abstractions from P vs NP conceptual pressures and difficulty hypotheses. Use when pressure localization has named bottlenecks such as verification-search gaps, hardness magnification ceilings, black-box substitution caps, MCSP/MKtP carrier debt, proof-complexity transfer, natural-proof pressure, relativization/algebrization barriers, advice leakage, padding/projection debt, or bounded-exponent windows, and the workflow needs candidate abstractions with proof obligations, falsifiers, symbolic probes, contradiction routes, and validation handoffs.
---

# P vs NP Pressure Bridge Forger

## Conceptual Role

Use this skill after `pvsnp-conceptual-pressure-localizer` and before committing a P vs NP branch to symbolic auditing, no-go theorem formation, or paper-level contribution assessment. Its job is to convert "why this is hard" into "what bridge abstraction could carry this difficulty without changing the theorem."

This is a generative abstraction-design skill with a deterministic scouting helper. Do not merely rename a pressure as an abstraction. A valid bridge abstraction must name source and target objects, the controlled interface between them, the invariant it preserves, the theorem-shaped obligation it creates, and the falsifier that would demote it.

## Workflow

1. **Read the pressure packet.**
   Identify the exact bottleneck: verification versus search, fixed-exponent versus all-polynomial separation, source-to-target transfer, naturalness, relativization, algebrization, advice leakage, padding/projection debt, proof-complexity certificate debt, or meta-complexity carrier debt.

2. **State the difficulty hypothesis.**
   Explain why the branch is hard in P vs NP objects. For example: a barely-superlinear carrier lower bound cannot exclude every SAT circuit exponent through a positive-query-length black-box interface; or a large constructive property risks becoming a natural proof.

3. **Forge bridge abstractions.**
   Propose one or more abstractions that could carry the pressure across regimes while preserving the target. Examples include:
   - a subpolynomial-query nonblackbox carrier bridge;
   - a searchable succinct MCSP/MKtP certificate bridge;
   - a proof-complexity lower-bound tautology bridge;
   - a sparse non-natural property bridge;
   - an all-exponent quantifier-lift bridge;
   - a route-specific impossibility theorem bridge.

4. **Type the bridge interface.**
   For each abstraction, state source object, target object, reduction or transfer interface, input-length map, circuit model, uniformity/advice status, quantifier order, barrier posture, and whether the bridge is meant to prove progress or produce a no-go theorem.

5. **Attach proof obligations and falsifiers.**
   Give a theorem-shaped obligation, the cheapest symbolic or literature check, and content-specific demotion conditions. A branch should not persist because it is interesting; it should persist because a named abstraction has a plausible target-preserving interface and an executable validation handoff.

6. **Choose the next skill.**
   Send formula-shaped obligations to `pvsnp-symbolic-complexity-auditor`, no-go-shaped abstractions to `pvsnp-impossibility-theorem-forger`, relation maps to `pvsnp-qualitative-complexity-reasoner`, and contribution-shaped subgoals to `paper-contribution-readiness-judge`.

## Bridge Patterns

- **Black-box ceiling to nonblackbox interface.** If substitution gives `N^{q+\beta c}`, then positive `\beta` yields only a bounded exponent window. A bridge must explain how `\beta=0`, `\beta=o(1)`, or nonblackbox use avoids plain oracle substitution without hiding advice.
- **Meta-complexity carrier to target lower bound.** If MCSP/MKtP is the carrier, the bridge must state threshold, truth-table length, verifier complexity, density, and why the carrier is not merely the target lower bound in disguise.
- **Proof-complexity certificate to uniform language.** A proof-like certificate bridge must specify the tautology family, proof system, verifier time, witness length, soundness meaning, and how accepted certificates produce a uniform target language.
- **Naturalness pressure to sparse/nonconstructive escape.** If usefulness, largeness, and constructivity all appear, the bridge must either accept natural-proof pressure or name a precise escape such as sparse valid lengths, non-large property, nonconstructive witness, or nonblackbox proof system.
- **Padding/projection debt to quantifier lift.** If the route only excludes `c < c_*`, the abstraction must say whether it can produce a cofinal family of source lower bounds or whether it should become a bounded no-go theorem.
- **Barrier pressure to impossibility theorem.** If the best contribution is negative, state a no-go theorem over a method class rather than pretending the route remains a direct proof path.

## Mathematical Invariants

- Mathematical object: pressure packet, difficulty hypothesis, bridge abstraction, source carrier, target class, transfer interface, quantifier pattern, barrier status, proof obligation, falsifier, and validation handoff.
- Preserved invariants: target statement, source and target complexity models, input-length map, uniform/nonuniform status, advice accounting, quantifier order, and target/proxy boundary.
- Broken invariants: replacing `P != NP` with a proxy lower bound without transfer, treating a fixed-exponent exclusion as all-polynomial separation, hiding advice inside the carrier, changing valid lengths without a certificate, or using a natural property while claiming barrier escape.
- Edge case or counterexample: subpolynomial-query interfaces, nonlarge properties, uniform-only lower bounds, promise carriers, oracle/algebraic variants, and proof-system-specific lower bounds may escape one abstraction and must be listed explicitly.

## Epistemic Discipline

Assign epistemic status: `bridge_candidate`, `typed_abstraction`, `proof_obligation`, `symbolic_probe_required`, `barrier_risk`, `no_go_candidate`, `contribution_shaped`, `adapt`, `backtrack`, `quarantined`, or `explicit_unknown`.

Cite KB IDs, cycle IDs, report sections, queue items, exact equations, prior-art anchors, validator outputs, or explicit unknowns for each substantive claim. Treat conceptual elegance as insufficient evidence until the bridge has a source object, target object, interface, and falsifier.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the bridge map. Run `scripts/build_pressure_bridges.py` to scout pressure signals from the P vs NP KB and marathon artifacts, inspect the emitted JSON or Markdown, and then add generative interpretation. The script is not a proof searcher; it is a typed inventory of bridge candidates and validation handoffs.

Example:

```bash
python skills/reasoning/pvsnp-pressure-bridge-forger/scripts/build_pressure_bridges.py
python agentic/scripts/validate_pvsnp_pressure_bridges.py
```

## Output Contract

Return:

1. `Pressure Source`: source artifact, branch, pressure type, and evidence.
2. `Difficulty Hypothesis`: why the route is hard in complexity-theoretic terms.
3. `Bridge Abstraction`: source object, target object, controlled interface, preserved invariant, and abstraction move.
4. `Proof Obligation`: theorem-shaped statement, variables, quantifiers, model, and side conditions.
5. `Falsifiers And Stop Conditions`: content-specific demotion tests and non-premature persistence criteria.
6. `Validation Handoff`: next skill, deterministic script, validator, literature check, queue item, or paper contribution task.
7. `Paper-Safe Narrative`: a concise way to describe the bridge without pipeline jargon.

## Failure/Demotion

Demote if the output only restates known barriers, cannot name source and target objects, hides quantifiers, lacks a falsifier, fails to distinguish proxy progress from target progress, or suggests another marathon cycle without a typed bridge obligation. Quarantine after sharpened attempts if no abstraction can preserve the target while escaping the named pressure.

## Validation Handoff

Validate generated bridge artifacts with `agentic/scripts/validate_pvsnp_pressure_bridges.py`. Use `pvsnp-symbolic-complexity-auditor` for exponent formulas, `pvsnp-impossibility-theorem-forger` for no-go versions, `contradiction-route-auditor` for proof-by-contradiction candidates, and `next-experiment-queue-ranker` for queue promotion.
