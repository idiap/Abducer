---
name: pvsnp-qualitative-complexity-reasoner
description: Build qualitative complexity-theoretic relation maps for P vs NP routes. Use when a branch needs to isolate variables, monotonicities, exponent transfers, asymptotic regimes, threshold behavior, density/naturalness conditions, verifier overhead, advice leakage, padding/projection growth, or meta-complexity carrier behavior without running unnecessary simulations.
---

# P vs NP Qualitative Complexity Reasoner

## Conceptual Role

Use this skill to understand how complexity-theoretic quantities move together. It gives the discovery loop a qualitative sense of direction: if query length grows, what exponent debt appears; if padding expands length, which target exponents are excluded; if a property is large and constructive, which natural-proof pressure increases.

This is not a numerical simulation skill. Most P vs NP qualitative structure should be estimated symbolically by relations, inequalities, quantifier checks, and asymptotic regimes. Use computation only for exact finite algebra, symbolic simplification, example sanity checks, or report validation.

## Workflow

1. **Identify the carrier and observable.**
   Name the source problem or carrier (`SAT`, `MCSP`, `MKtP`, truth-table property, projection carrier, padded language, proof-complexity object) and the response quantity being tracked.

2. **Build a variable frame.**
   Record variables such as input length `n`, carrier length `N`, circuit size exponent `c`, source threshold exponent `a`, reduction overhead `q`, target-query exponent `beta`, padding exponent `k`, advice bits, verifier overhead, density, constructivity time, promise density, and error/slack terms.

3. **Separate independent knobs from derived responses.**
   Mark what can vary freely and what is determined by reduction geometry, padding, verifier construction, oracle access, or circuit simulation.

4. **Derive directional relations.**
   State whether increasing one quantity increases, decreases, saturates, preserves, or invalidates another under held-fixed conditions. Include threshold effects such as `beta=0` versus `beta>0`, bounded-exponent exclusion versus all-polynomial exclusion, and dense versus sparse valid lengths.

5. **Map regimes and noncommuting limits.**
   Specify fixed-exponent, all-exponent, uniform, nonuniform, sparse-length, oracle, algebraic, promise, average-case, and meta-complexity regimes. Warn when changing the regime changes the target.

6. **Produce graph-ready relations.**
   Emit nodes and edges with signs, regimes, assumptions, falsifiers, and what the edge would teach the global problem.

## Mathematical Invariants

- Mathematical object: source carrier, target class, variables, transfer inequality, asymptotic regime, barrier status, and relation graph edge.
- Preserved invariants: model identity, input-length map, uniform/nonuniform status, quantifier order, held-fixed assumptions, and target/proxy distinction.
- Broken invariants: treating a derived overhead as an independent knob, suppressing advice bits, conflating `n` and `N`, using fixed-exponent evidence for all-exponent separation, or replacing a lower-bound threshold with a slogan about hardness magnification.
- Edge case or counterexample: if `N=n^k`, a lower bound in `N^a` may translate only to `n^{ak}`; if the transfer under `SAT in SIZE(n^c)` gives `N^{q+beta c+o(1)}`, then positive `beta` may leave only a bounded target-exponent window.

## Epistemic Discipline

Assign epistemic status to each relation: `typed`, `partially_typed`, `symbolically_estimated`, `proof-obligation`, `barrier-risk`, `proxy-risk`, `blocked`, `refuted`, `promoted`, `quarantined`, or `explicit_unknown`.

Cite cycle IDs, KB IDs, equations, report sections, queue items, source artifacts, or explicit unknowns. Do not promote a qualitative edge unless held-fixed conditions, validity regime, and falsifier are stated.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the qualitative map. Prefer symbolic or deterministic checks over simulation. Appropriate commands include report generation/validation, exact algebra with SymPy for transfer formulas, and qualitative graph validators. Inspect outputs before interpreting them.

## Output Contract

Return:

1. `Carrier And Target`: source object, target class, model, and proof obligation.
2. `Variable Frame`: independent variables, dependent responses, hidden couplings, allowed ranges, and held-fixed conditions.
3. `Qualitative Relations`: directional edges, monotonicities, thresholds, asymptotic regimes, and invalidating cases.
4. `Transfer Formula Sketch`: symbolic inequality or relation, even if conjectural, with exact unknowns.
5. `Mechanistic Graph Update`: graph-ready nodes, edges, labels, and explanation for an end user.
6. `Falsifiers`: computations, theorem checks, barrier checks, or counterexamples that would demote the relation.
7. `Validation Handoff`: next skill, graph artifact, validator, or proof obligation.

## Failure/Demotion

Demote if variables are only listed as nouns, if `n`/`N` or uniform/nonuniform regimes are confused, if the relation lacks held-fixed assumptions, if a target separation becomes a proxy, or if a graph edge has no falsifier. Quarantine relation packets that cannot state a model and quantifier regime.

## Validation Handoff

Hand pressure-laden branches back to `pvsnp-conceptual-pressure-localizer`, no-go candidates to `pvsnp-impossibility-theorem-forger`, and report/graph updates to the marathon renderer plus `agentic/scripts/validate_discovery_marathon_report.py`. If qualitative graph packet files exist, validate them with `agentic/scripts/validate_qualitative_relation_packets.py` and `agentic/scripts/validate_qualitative_mechanistic_graph.py`.
