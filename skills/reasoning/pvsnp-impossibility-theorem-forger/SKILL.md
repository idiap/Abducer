---
name: pvsnp-impossibility-theorem-forger
description: Forge proof-by-contradiction and impossibility/no-go theorem candidates for P vs NP strategy branches. Use when a route may be more valuable as a barrier-aware obstruction theorem than as direct proof search, including black-box substitution caps, padding/projection debt, natural-proof pressure, relativizing or algebrizing limitations, advice leakage, or meta-complexity carrier no-go results.
---

# P vs NP Impossibility Theorem Forger

## Conceptual Role

Use this skill when a P vs NP branch is likely to clarify what cannot work. The goal is to turn failed or suspicious route families into precise contradiction routes or impossibility theorems with assumptions, conclusions, proof skeletons, and non-claim boundaries.

This is a generative proof-design skill. Do not merely say "this is impossible by known barriers." State the route family, assumptions, exact contradiction or no-go conclusion, and the weakest condition under which the theorem would be true.

## Workflow

1. **State the route family.**
   Name the family being tested: black-box SAT substitution, padding/projection magnification, meta-complexity carrier transfer, natural-property lower-bound route, relativizing diagonalization, algebrizing method, or nonuniform advice-dependent route.

2. **Choose the logic form.**
   Use proof by contradiction when the target is a positive claim whose negation has structure. Use an impossibility/no-go theorem when the object is a route family: "No method with properties A, B, C can imply target T."

3. **Formalize assumptions.**
   State source lower-bound assumption, target class, reduction interface, query-length exponent, constructivity, largeness, oracle/algebraic access, advice model, padding map, and quantifier order.

4. **Derive the obstruction.**
   Generate the critical consequence: exponent window cap, natural-proof conflict, relativizing oracle separation, algebrization boundary, sparse-valid-length debt, advice leakage, or source lower bound as hard as the target.

5. **State theorem-shaped result.**
   Emit theorem title, hypotheses, conclusion, proof skeleton, examples covered, examples not covered, and a precise non-claim boundary.

6. **Audit before promotion.**
   Send the theorem candidate to `contradiction-route-auditor` for exact negation, same-model preservation, conflict target, excluded cases, and non-vacuity.

## Contradiction And No-Go Patterns

- **Black-box substitution cap:** Assume a route uses target circuits through queries of length `n^beta` and reduction overhead `N^q`; derive that `SAT in SIZE(n^c)` gives the carrier upper bound `N^{q+beta c+o(1)}`, so positive `beta` cannot exclude every polynomial `c`.
- **Padding/projection debt:** Assume padding length `N=n^k` or a sparse valid-length carrier; show the claimed magnification either yields a bounded exponent window or requires sparse-length lower bounds carrying the original difficulty.
- **Natural property obstruction:** Assume the route defines a large, constructive, useful property against a circuit class supporting pseudorandom functions; derive the natural-proofs pressure and name the escape condition.
- **Relativization/algebrization boundary:** Assume the method is oracle-respecting or algebraic-query-respecting; compare with known barrier behavior and state what nonrelativizing/nonalgebrizing ingredient is missing.
- **Advice leakage no-go:** Assume the transfer enters `P/poly` or advice-bearing carriers; show where nonuniform advice can absorb the intended lower-bound witness.

## Mathematical Invariants

- Mathematical object: route family, exact target, negated or bounded method claim, assumptions, obstruction carrier, conflict target, theorem conclusion, proof obligations, and non-claim boundary.
- Preserved invariants: same complexity model, same source and target classes, same reduction interface, same quantifier order, same oracle/algebraic status, and explicit advice/uniformity status.
- Broken invariants: proving a no-go for black-box methods while claiming to refute nonblackbox methods, using natural-proof barriers without largeness and constructivity checks, treating oracle barriers as absolute impossibility, or deriving a contradiction against a theorem that is not accepted in the active model.
- Edge case or counterexample: a genuinely nonblackbox carrier, subpolynomial target-query interface, non-large/nonconstructive property, uniform-only method, or proof-complexity route may escape the no-go and must be listed rather than silently ruled out.

## Epistemic Discipline

Assign epistemic status: `theorem_candidate`, `proof-obligation`, `barrier-backed`, `partial_no_go`, `escape_condition_found`, `blocked`, `refuted`, `promoted`, `quarantined`, or `explicit_unknown`.

Cite KB IDs, cycle IDs, timeline report sections, queue items, equations, prior-art anchors, validator outputs, or explicit unknowns. Distinguish accepted barrier theorems from heuristic barrier analogies.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground a theorem candidate. Use deterministic validation for report consistency, queue insertion, and theorem packet presence; use symbolic algebra only for exact transfer simplification. Inspect artifacts before interpreting them.

## Output Contract

Return:

1. `Route Family`: method class, source object, target class, and evidence source.
2. `Logic Form`: contradiction route, impossibility theorem, obstruction lemma, or barrier audit.
3. `Formal Statement`: theorem title, hypotheses, conclusion, quantifiers, model, and non-claim boundary.
4. `Proof Skeleton`: steps, derived consequence, conflict target, and where each assumption is used.
5. `Escape Conditions`: what method variants are not ruled out and why.
6. `Proof Obligations`: lemmas, prior-art checks, exact calculations, and definitions still needed.
7. `Disposition`: promote to proof queue, adapt, backtrack, pivot, quarantine, or reject.
8. `Validation Handoff`: next auditor, validator, report section, queue item, or paper contribution task.

## Failure/Demotion

Demote when the theorem is merely rhetorical, rules out more than its hypotheses justify, lacks quantifiers, misses known escape conditions, relies on an unaccepted conflict target, or does not say how it bears on `P != NP` or `NP not subset P/poly`. Quarantine if the no-go theorem only restates a known barrier without a new route-specific obstruction.

## Validation Handoff

Hand every candidate to `contradiction-route-auditor`, then to `paper-contribution-readiness-judge` if it becomes contribution-shaped. Route qualitative parameter gaps to `pvsnp-qualitative-complexity-reasoner` and conceptual hardness gaps to `pvsnp-conceptual-pressure-localizer`. Use `agentic/scripts/validate_discovery_marathon_report.py` after report-facing integration.
