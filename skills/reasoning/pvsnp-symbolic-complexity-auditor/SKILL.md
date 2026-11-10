---
name: pvsnp-symbolic-complexity-auditor
description: Perform exact symbolic and CAS-assisted audits for P vs NP discovery routes. Use when a branch needs exponent-transfer algebra, padding/projection bookkeeping, finite truth-table or circuit-count sanity checks, natural-proof largeness/constructivity tests, advice/uniformity accounting, oracle/barrier signature ledgers, or bounded symbolic probes that clarify whether a P vs NP strategy should persist, pivot, or become an impossibility theorem.
---

# P vs NP Symbolic Complexity Auditor

## Conceptual Role

Use this skill when qualitative complexity reasoning has produced a concrete formula-shaped obligation. The aim is not to let a CAS search for a proof of P vs NP. The aim is to make route claims exact enough that the discovery loop can stop repeating slogans and decide whether a branch has a target-preserving transfer, a bounded no-go theorem, or a hidden model switch.

For this problem, symbolic reasoning is valuable in six narrow regimes:

1. **Exponent-transfer algebra.** Compute how `SAT in SIZE(n^c)` or `NP subset P/poly` propagates through a carrier with overhead `q`, target-query exponent `beta`, padding exponent `k`, and source lower-bound exponent `a`.
2. **Padding and projection bookkeeping.** Track maps such as `N=n^k`, sparse valid lengths, projection overhead, and whether an advertised weak lower bound really excludes all polynomial SAT exponents or only a bounded window.
3. **Finite carrier sanity checks.** Enumerate tiny Boolean functions, truth-table lengths, or circuit-count upper bounds only to test definitions, density, constructivity, and toy counterexamples.
4. **Natural-proof pressure.** Symbolically record largeness, constructivity time, usefulness class, and pseudorandom-function assumptions; do not call a property non-natural without checking which condition fails.
5. **Advice and uniformity accounting.** Make advice bits, nonuniform circuit families, uniform reductions, and verifier overhead explicit in the same formula.
6. **Barrier-signature ledgers.** Encode whether the reasoning relativizes, algebrizes, naturalizes, or relies on a nonblackbox ingredient that escapes a known barrier hypothesis.

## Workflow

1. **Select the symbolic carrier.**
   Name the route family: hardness magnification, MCSP/MKtP carrier, padding/projection carrier, proof-complexity route, derandomization/PIT route, diagonalization, or barrier audit.

2. **State variables and quantifiers.**
   Record `n`, `N`, `c`, `a`, `q`, `beta`, padding exponent `k`, circuit class, advice bits, oracle/algebraic access, density, constructivity time, and target conclusion. Mark which are fixed constants and which are quantified over all polynomials.

3. **Choose symbolic mode.**
   Use:
   - exact rational algebra for exponent windows;
   - SymPy simplification for transfer expressions, recurrences, inequalities, and asymptotic expressions;
   - finite enumeration only for toy carriers or definition checks;
   - barrier ledgers for non-computational symbolic statuses.

4. **Run bounded computation only after typing the claim.**
   For exponent-transfer audits, prefer:
   `python skills/reasoning/pvsnp-symbolic-complexity-auditor/scripts/audit_transfer.py --a 1.1 --q 1 --beta 0.25 --padding-k 1`
   or pass a JSON spec with `--spec path/to/spec.json`.

5. **Interpret the symbolic result generatively.**
   Explain whether the formula gives:
   - all-polynomial exclusion potential;
   - bounded-exponent-only evidence;
   - no contradiction because overhead already dominates;
   - a projection/padding demagnification;
   - a barrier/no-go theorem candidate;
   - an exact unknown requiring literature or proof-theoretic input.

6. **Hand off to the right next skill.**
   Send parameter relations to `pvsnp-qualitative-complexity-reasoner`, no-go statements to `pvsnp-impossibility-theorem-forger`, pressure explanations to `pvsnp-conceptual-pressure-localizer`, and queue decisions to `next-experiment-queue-ranker`.

## Mathematical Invariants

- Mathematical object: source carrier, target class, reduction interface, exact transfer formula, quantified exponent window, barrier status, and proof obligation.
- Preserved invariants: source/target model identity, uniform/nonuniform status, input-length map, held-fixed assumptions, advice accounting, oracle/algebraic status, and quantifier order.
- Broken invariants: treating fixed-exponent exclusion as `P != NP`, hiding advice in the carrier, conflating `n` and `N`, letting padding change the target theorem, or promoting finite enumeration beyond toy-definition sanity checks.
- Edge case or counterexample: if `beta>0`, a source lower bound `N^a` against an induced upper bound `N^{q+beta c+o(1)}` excludes at most `c < (a-q)/beta`; this is not `NP not subset P/poly`.

## CAS Discipline

Use CAS as a proof-control instrument, not as discovery theater.

- Appropriate: simplifying transfer inequalities, solving exponent windows, checking exact small-count formulas, deriving recurrence closed forms, and validating symbolic side-condition ledgers.
- Inappropriate: unbounded random search, brute-force claims about P vs NP, large empirical simulation presented as evidence for separation, or theorem-prover claims without a separate proof workflow.
- Required interpretation: every CAS output must state variables, assumptions, target class, validity regime, what it proves, and what it does not prove.

## Epistemic Discipline

Assign epistemic status to each symbolic result: `exact_transfer_audit`, `symbolically_estimated`, `toy_finite_check`, `barrier_ledger`, `proof_obligation`, `bounded_no_go_candidate`, `promoted`, `adapt`, `backtrack`, `quarantined`, or `explicit_unknown`.

Cite evidence for every symbolic claim: cycle IDs, KB IDs, route names, source artifacts, exact command outputs, JSON specs, report sections, prior-art anchors, or explicit unknowns. Treat the script output as evidence about a typed transfer formula, not as evidence that P vs NP has been decided.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when running the helper script or any CAS-backed check. Execute the smallest typed probe that decides the current branch question, inspect the JSON output, and then write a generative interpretation that names the target class, side conditions, non-claims, and next validation handoff.

Do not leave deterministic output uninterpreted. If the helper reports `bounded_exponent_window_only`, explain which route becomes a no-go candidate and which escape conditions remain. If it reports `potential_all_polynomial_exclusion`, send the branch through advice, naturalness, relativization, algebrization, and nonblackbox audits before promotion.

## Output Contract

Return:

1. `Symbolic Carrier`: route family, source object, target object, and model.
2. `Variable Ledger`: exact variables, fixed/quantified status, allowed ranges, and hidden couplings.
3. `Transfer Formula`: simplified formula, side conditions, and exact exponent window.
4. `CAS Or Exact Probe`: command or calculation used, output summary, and reproducibility path.
5. `Conceptual Interpretation`: what the symbolic result means for the route.
6. `Barrier And Model Ledger`: relativization, algebrization, naturalness, advice, and uniformity status.
7. `Disposition`: promote, adapt, backtrack, pivot, quarantine, or convert into an impossibility theorem.
8. `Validation Handoff`: validator, next skill, report artifact, or paper/theorem task.

## Failure/Demotion

Demote if the calculation lacks a typed source and target, hides a quantifier, uses decimals when exact rational data are available, says "CAS proves" without a theorem statement, or interprets a bounded exponent window as a main-target result. Quarantine symbolic probes that cannot name their transfer theorem, falsifier, or barrier boundary.
